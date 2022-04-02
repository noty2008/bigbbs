#! c:/perl64/bin/perl
package data;

use File::Path;

#データの初期化
# 戻り値: 0 成功
sub init{
	if(-e $ini::data){
		# ディレクトリがあれば消す
		rmtree($ini::data);
		
	}
	mkdir $ini::data;
	open FH, ">$ini::data/threads.cgi";
	print FH "1";
	close FH;
	chmod $ini::filePermission, "$ini::data/threads.cgi";
	open FH, ">$ini::data/waste.cgi";
	close FH;
	chmod $ini::filePermission, "$ini::data/waste.cgi";

	if(-e "$ini::data/threads.cgi" && -e "$ini::data/waste.cgi"){
		return 0;
	}else{
		return 1;
	}
}
# ファイルの復旧
sub restore{
	my($mode);
	if((-e "$ini::data/threads.cgi")&&(-e "$ini::data/waste.cgi")){
		return 1;
	}
	if(!(-e "$ini::data/threads.cgi")&&(-e "$ini::data/waste.cgi")){
		$mode=0;
	}
	if((-e "$ini::data/threads.cgi")&&!(-e "$ini::data/waste.cgi")){
		$mode=1;
	}
	if(!(-e "$ini::data/threads.cgi")&&!(-e "$ini::data/waste.cgi")){
		$mode=2;
	}
	my(@threads)=();
	my(@waste)=();
	my($i);
	for($i=1;-e "$ini::data/$i.cgi";$i++){
		open FILE,"$ini::data/$i.cgi";
		next if(exists $dts{$i});
		my($thread)=loadthread($i);
		if($thread->{'alive'}==1){
			my($linedata)={};
			$linedata->{'number'}=$i;
			$linedata->{'title'}=$thread->{'title'};
			$linedata->{'maker'}=$thread->{'maker'};
			my($reses)=$thread->{'res'};
			my($date)=${$reses}[0]->{'date'};
			if($date =~ /;(.+?)$/){
				$date=$1;
			}
			$linedata->{'mdate'}=$date;
			$linedata->{'date'} = ${$reses}[$#{$reses}]->{'date'};
			$linedata->{'lastreply'} = ${$reses}[$#{$reses}]->{'name'};
			$linedata->{'resnum'}=scalar grep{$_->{'flag'}==0}(@{$reses});

			unshift @threads,makethreadlistdata($linedata);
		}else{
			my($linedata)={};
			$linedata->{'number'}=$i;
			$linedata->{'title'}=$thread->{'title'};
			$linedata->{'date'}="??? 復旧:".time_str();
			$linedata->{'etc'}="???";
			unshift @waste,makewastelistdata($linedata);
		}
	}
	unshift @threads,"$i\n";
	if(($mode==0)||($mode==2)){
		open(FILE,">$ini::data/threads.cgi");
		foreach(@threads){
			chomp;
			print FILE "$_\n";
		}
		close(FILE);
	}
	if(($mode==1)||($mode==2)){
		open(FILE,">$ini::data/waste.cgi");
		foreach(@waste){
			chomp;
			print FILE "$_\n";
		}
		close(FILE);
	}
	return 0;
}

# ファイルシステムのテスト
# 正常なら1・だめなら0
sub test{
	unless(-e $ini::data){
		return 0;
	}
	unless(-e "$ini::data/threads.cgi"){
		return 0;
	}
	unless(-e "$ini::data/waste.cgi"){
		return 0;
	}
	return 1;
}

# ファイルロック
# 戻り値:1→成功 0→失敗
sub filelock{
	my($retry)=5;
	my($suc)=1;
	while(!mkdir("$ini::data/$ini::lockdir", 0755)){
		if(--$retry <= 0){
			# まだかな
			if((-M "$ini::data/$ini::lockdir")*86400 >= 60){
				# タイムオーバー
				fileunlock();
				$suc=1;
				last;
			}else{
				# だめ
				$suc=0;
				last;
			}
		}
	}
	return $suc;
}
sub fileunlock{
	rmdir("$ini::data/$ini::lockdir");
}
#--------------------------------------
# スレッド一覧
sub threads_table{
	my($page)=shift;	#-1なら管理者モード
	#データファイルオープン
	unless(open(FILE,"$ini::data/threads.cgi")){
		output::error2("ファイルを開くことができませんでした。");
		return 0;
	}
	my(@th)=<FILE>;
	shift @th;
	my($i)=0;

	if($::top_mode eq "table"){
		output::threads_table_header($page,scalar @th);
		foreach(@th){
			if($page>=0){
				if($i<$page){
					$i++;
					next;
				}
				last if($i>($page-1+$ini::page_threads));
			}
			chomp;
			output::threads_thread(getthreadlistdata($_));
			$i++;
		}
		close(FILE);
		output::threads_table_footer($page,scalar @th);
	}elsif($::top_mode eq "open"){
		output::threads_header();
		if($page>=0){
			output::threads_navi($page,scalar @th,'up');
		}
		foreach(@th){
			if($page>=0){
				if($i<$page){
					$i++;
					next;
				}
				last if($i>($page-1+$ini::page_threads));
			}
			chomp;
			my($thdata)=getthreadlistdata($_);
			view($thdata->{'number'},0,$cgi,"latest");
			$i++;
		}
		close(FILE);
		output::threads_footer();
	}
	return 1;
}
#記事を表示
sub view{
	my($number,$page,$cgi,$mode)=@_;
	#$mode :"normal" → 記事表示ページ（ページ全部）
	#	"latest" → 新しいとこだけ（記事単体）
	if(testthread($number)==0){
		output::error1("ファイルを開くことができませんでした。");
		return;
	}
	$data = loadthread($number);
	if($data->{'alive'}==0 && $::Global_admin_mode==0){
		output::error1("このスレッドは削除されています。");
		return;
	}
	filelock();

	if($mode eq "normal"){
		# 参照数を1増やす
		my(@threads)=loadthreadslist();
		my($nextth)=int(shift @threads);
		my($i)=0;
		foreach(@threads){
			if($_ =~ /^$number\t/){
				my($thl)=getthreadlistdata($_);
				$thl->{'seen'}++;
				splice @threads, $i, 1, makethreadlistdata($thl);
			}
			$i++;
		}
		unshift @threads,$nextth;
		savethreadslist(@threads);
		fileunlock();
	}

	my($st,$en)=(-1,1000000);
	if($mode eq "normal"){
		output::view_header($data);
		my($resn)=$cgi->param('res');
		if($resn =~ /^(\d*)(-?)(\d*)$/){
			if($2 eq "" && $1 ne ""){
				$st=$en=int($1);
			}elsif($2 ne ""){
				if($1 ne ""){
					$st=int($1);
				}else{
					$st=0;
				}
				if($3 ne ""){
					$en=int($3);
				}else{
					$en=@{$data->{'res'}};
				}
			}
		}
		
	}elsif($mode eq "latest"){
		output::view_article($data);
		$en=$data->{'nextres'}-1;
		$st=$en-$ini::page_res+1;
		$st=0 if($st<0);
	}

	# レス

	if(($::Global_admin_mode==0)&&($mode eq "normal")){
		my($v_res_number) = scalar grep { $_->{'flag'}==0 }(@{$data->{'res'}});	# 可視のレスの数

		output::view_navi($number,$page,$v_res_number,'up');
	}

	$i=0;
	foreach(@{$data->{'res'}}){
		if($st==-1){
			if($page>=0){
				if($i<$page){
					$i++ if($_->{'flag'}==0);
					next;
				}
				last if($i>=($page+$ini::page_res));
			}
		}
		if($_->{'flag'}==0 || $::Global_admin_mode==1){
			if($_->{'num'}==1 && $mode eq "latest"){
				output::res($_,undef,$number);
				$i++;
			}elsif($_->{'num'} >= $st && $_->{'num'} <= $en){
				output::res($_,undef,$number);
				$i++;
			}
		}
	}
	if($::Global_admin_mode==0 && $mode eq "normal"){
		output::view_navi($number,$page,$v_res_number,'down');
	}
	output::view_footer();
	if($mode eq "normal"){
		if($::Global_admin_mode==0){
			output::view_reply($number,$data,$cgi);
		}
		if($::Global_admin_mode==1 || $ini::delete_free!=0){
			output::view_delete($number);
		}
		if($::Global_admin_mode==1){
			if($data->{'alive'}==1){
				output::view_thdelete($number);
			}else{
				output::view_threstore($number);
			}
		}
		output::footer();
	}
}

# スレッドファイルのテスト
sub testthread{
	$number=shift;
	if(-e "$ini::data/$number.cgi"){
		return 1;
	}else{
		return 0;
	}
}
# スレッド一覧を読み込む
sub loadthreadslist{
	open(FILE,"$ini::data/threads.cgi");
	my(@lines)=<FILE>;
	close(FILE);
	return @lines;
}
# スレッド一覧を書き込む
sub savethreadslist{
	open(FILE,">$ini::data/threads.cgi");
	foreach(@_){
		chomp;
		print FILE "$_\n";
	}
	close(FILE);
}

# スレッドファイルを読み込む
sub loadthread{
	my($number)=shift;
	my(%data)=();
	my($line);
	open(FILE,"$ini::data/$number.cgi");
	# 1行目
	$line=<FILE>;
	chomp $line;
	my($title, $maker, $resnum,$alive) = split(/\t/,$line);
	$data{'title'}=$title;
	$data{'maker'}=$maker;
	$data{'nextres'}=$resnum;
	$data{'alive'}=$alive;

	$data{'number'}=$number;

	my(@res)=();
	my($mode)=0;
	my($nowline);
	my($ls);
	while(<FILE>){
		if($mode==0){
			chomp;
			next if($_ eq "");
			$nowline = {};
			push @res, $nowline;
			($nowline->{'num'},$nowline->{'name'},$nowline->{'title'},$nowline->{'date'},$nowline->{'date2'},$nowline->{'url'},$nowline->{'email'},$nowline->{'color'})=split(/\t/);

			$mode=1;
		}elsif($mode==1){
			chomp;
			($nowline->{'ip'},$nowline->{'host'},$nowline->{'password'},$nowline->{'flag'},$nowline->{'message_lines'})=split(/\t/);
			$mode=2;
			$nowline->{'message'}="";
			$ls=0;
		}elsif($mode==2){
			#本文
			$nowline->{'message'}.=$_;
			if($_ eq "\n" && $ls>=$nowline->{'message_lines'}){
				do{}while(chomp $nowline->{'message'});
				$mode=0;
			}
			$ls++;
		}
	}
	$data{'res'}=\@res;
	close(FILE);
	return \%data;
}
# スレッドファイルを書き込む
sub savethread{
	my($number,$data)=@_;
	open(FILE,">$ini::data/$number.cgi");
	# 1行目
	print FILE $data->{'title'}."\t".$data->{'maker'}."\t".$data->{'nextres'}."\t".$data->{'alive'}."\n";

	foreach(@{$data->{'res'}}){
		print FILE join("\t",($_->{'num'},$_->{'name'},$_->{'title'},$_->{'date'},$_->{'date2'},$_->{'url'},$_->{'email'},$_->{'color'}))."\n";
		print FILE join("\t",($_->{'ip'},$_->{'host'},$_->{'password'},$_->{'flag'},$_->{'message_lines'}))."\n";
		print FILE $_->{'message'}."\n\n";
	}
	close(FILE);
}
# 返信処理
# 戻り値 成功→1 失敗→0
sub reply{
	my($number,$cgi)=@_;
	unless(testthread($number)){
		output::error1("そのスレッドは存在しません。");
		return 0;
	}
	my($tr)=testreplydata($cgi);
	if($tr==1){
		output::error1("入力漏れがあります。");
		return 0;
	}
	if($tr==2){
		output::error1("使用できない言葉が含まれています。");
		return 0;
	}
	unless(filelock()){
		output::error1("現在混雑しています。");
		return 0;
	}
	my(@threadslist)=loadthreadslist();
	my($thread)=loadthread($number);

	my($i)=0;
	my($thl);
	foreach(@threadslist){
		if($_ =~ /^$number\t/){
			$thl = getthreadlistdata($_);
			splice @threadslist,$i,1;
			last;
		}
		$i++;
	}
	$thl->{'resnum'}++;

	# 書き込み
	my($res)=makeresdata($cgi,$thread->{'nextres'});
	push(@{$thread->{'res'}},$res);
	$thread->{'nextres'}++;

	$thl->{'date'}=$res->{'date'};
	$thl->{'lastreply'}=$res->{'name'};

	my($nextthread)=shift @threadslist;	# 先頭は次のスレッド番号
	unshift @threadslist,makethreadlistdata($thl);
	unshift @threadslist, $nextthread;
	savethreadslist(@threadslist);

	savethread($number,$thread);

	
	fileunlock();

	return 1;
}
# threads.cgiの1行分のデータを作る
sub makethreadlistdata{
	my($data)=shift;
	return $data->{'number'}."\t".$data->{'title'}."\t".$data->{'resnum'}."\t".$data->{'maker'}."\t".$data->{'mdate'}."\t".
	$data->{'date'}."\t".$data->{'lastreply'}."\t".$data->{'seen'}."\n";
}
# 1行からデータを得る
sub getthreadlistdata{
	my($line)=shift;
	chomp $line;
	my($data)={};
	($data->{'number'},$data->{'title'},$data->{'resnum'},$data->{'maker'},$data->{'mdate'},
	$data->{'date'},$data->{'lastreply'},$data->{'seen'}) = split(/\t/,$line);
	return $data;
}
# waste.cgiの1行分のデータを作る
sub makewastelistdata{
	my($data)=shift;
	return $data->{'number'}."\t".$data->{'title'}."\t".$data->{'date'}."\t".$data->{'etc'}."\t".$data->{'seen'}."\n";
}
sub getwastelistdata{
	my($line)=shift;
	chomp $line;
	my($data)={};
	($data->{'number'},$data->{'title'},$data->{'date'},$data->{'etc'},$data->{'seen'})=split(/\t/,$line);
	return $data;
}
sub makeresdata{
	my($cgi,$resnumber)=@_;
	my($data)={};
	my($message)="";
	my(@lines)=split(/\r\n|\r|\n/,safevalue($cgi->param('message')));
	foreach(@lines){
		chomp;
		$message.="$_\n";
	}
	$message =~ s/\n+\Z//g;

	my($myname) = getname($cgi->param('name'));
	$data->{'message'}=$message;
	$data->{'title'}=safevalue($cgi->param('title'));
	$data->{'name'}=$myname;
	$data->{'password'}=$cgi->param('password');
	$data->{'message_lines'} = scalar split(/\n/,$message);

	if($ini::use_URL){
		$data->{'url'}=$cgi->param('url');
	}else{
		$data->{'url'}="";
	}
	if($ini::use_email){
		$data->{'email'}=$cgi->param('email');
	}else{
		$data->{'email'}="";
	}
	if($ini::use_color>0){
		$data->{'color'}=$cgi->param('color');
	}else{
		$data->{'color'}="";
	}

	$data->{'flag'}=0;

	my($ip)=$data->{'ip'}=$ENV{'REMOTE_ADDR'};
	$data->{'host'}=gethostbyaddr(pack("C4",split(/\./,$ip)), 2);

	$data->{'date'}=time_str();
	$data->{'date2'}=time;

	$data->{'num'}=$resnumber;

	return $data;
}
# レスを消す処理
sub deleteres{
	my($cgi)=shift;
	my($number)=int($cgi->param('number'));
	unless(testthread($number)){
		output::error1("そのスレッドは存在しません。");
		return 0;
	}
	my($res_number)=int($cgi->param('res_number'));
	if($res_number==1){
		output::error1("スレッドの最初のレスは削除できません。");
		return 0;
	}
	unless(filelock()){
		output::error1("現在混雑しています。");
		return 0;
	}
	my(@threadslist)=loadthreadslist();
	my($thread)=loadthread($number);

	my($flg,$i)=(0, 0);
	foreach(@{$thread->{'res'}}){
		if(($_->{'num'} == $res_number)&&($_->{'flag'}==0)){
			if(checkpassword($_->{'password'},$cgi->param('password'))){
				# OK
				$_->{'flag'} = 1;	# 削除済みにする
				$_->{'date'} = "(削除)".time_str().";".$_->{'date'};
				my($j)=0;
				foreach(@threadslist){
					if($_ =~ /^$number\t/){
						my($thl)=getthreadlistdata($_);
						$thl->{'resnum'}--;
						splice @threadslist,$j,1,makethreadlistdata($thl);
						last;
					}
					$j++;
				}
				$flg=1;
				last;
			}else{
				# NG
				output::error1("パスワードが違います。");
				$flg=2;
				last;
			}
		}

		$i++;
	}
	if($flg==0){
		output::error1("レス番号が不正です。");
	}
	if($flg==1){
		savethreadslist(@threadslist);
		savethread($number,$thread);
	}
	fileunlock();
	return 1 if($flg==1);
	return 0;
}
# レス編集準備
sub editres_init{
	my($cgi)=shift;
	my($number)=int($cgi->param('number'));
	unless(testthread($number)){
		output::error1("そのスレッドは存在しません。");
		return 0;
	}
	my($thread)=loadthread($number);
	my($res_number)=int($cgi->param('res_number'));
	my($flg,$i)=(0, 0);
	foreach(@{$thread->{'res'}}){
		if(($_->{'num'} == $res_number)&&($_->{'flag'}==0)){
			if(checkpassword($_->{'password'},$cgi->param('password'))){
				# OK
				output::editres($number,$res_number,$thread,$_,$cgi->param('password'));
				$flg=1;
				last;
			}else{
				# NG
				output::error1("パスワードが違います。");
				$flg=2;
				last;
			}
		}

		$i++;
	}
	if($flg==0){
		output::error1("レス番号が不正です。");
	}
	return 1 if($flg==1);
	return 0;
}
# レス編集
sub editres_do{
	my($cgi)=shift;
	my($number)=int($cgi->param('number'));
	unless(testthread($number)){
		output::error1("そのスレッドは存在しません。");
		return 0;
	}
	my($res_number)=int($cgi->param('res_number'));
	unless(filelock()){
		output::error1("現在混雑しています。");
		return 0;
	}
	my($thread)=loadthread($number);
	my($flg,$i)=(0, 0);
	foreach(@{$thread->{'res'}}){
		if(($_->{'num'} == $res_number)&&($_->{'flag'}==0)){
			if(checkpassword($_->{'password'},$cgi->param('old_password'))){
				# OK
				$_->{'flag'}=2;
				my($newres) = makeresdata($cgi,$_->{'num'});
				if($_->{'date'} =~ /^\(編集(\d*)\)/){
					my($m)=int($1);
					$m=1 if($m<1);
					$m++;
					$newres->{'date'}= "(編集$m)" . $newres->{'date'};
				}else{
					$newres->{'date'}= "(編集)" . $newres->{'date'};
				}
				splice @{$thread->{'res'}}, $i+1, 0, $newres;
				$flg=1;
				last;
			}else{
				# NG
				output::error1("パスワードが違います。");
				$flg=2;
				last;
			}
		}

		$i++;
	}
	if($flg==0){
		output::error1("レス番号が不正です。");
	}
	if($flg==1){
		savethread($number,$thread);
	}
	fileunlock();
	return 1 if($flg==1);
	return 0;
}
#新スレ処理
#戻り値 スレ番号（エラーなら-1）
sub newthread{
	my($cgi)=shift;
	my($tr)=testreplydata($cgi);
	if($tr==1){
		output::error1("入力漏れがあります。");
		return 0;
	}
	if($tr==2){
		output::error1("使用できない言葉が含まれています。");
		return 0;
	}
	unless(filelock()){
		output::error1("現在混雑しています。");
		return -1;
	}
	my(@threadslist)=loadthreadslist();
	my($number)=int(shift @threadslist);

	# 新しいスレのデータを作る
	my($myname) = getname($cgi->param('name'));
	my($mytitle)=safevalue($cgi->param('title'));

	my($data)={};
	$data->{'number'}=$number;
	$data->{'title'}=$mytitle;
	$data->{'resnum'}=0;
	$data->{'alive'}=1;
	$data->{'maker'}=$data->{'lastreply'}=$myname;
	$data->{'mdate'}=$data->{'date'}=time_str();
	$data->{'seen'}=0;

	my($thread)={};
	

	$thread->{'title'}=$mytitle;
	$thread->{'maker'}=$myname;
	$thread->{'nextres'}=1;
	$thread->{'alive'}=1;
	$thread->{'res'} = [];

	unshift @threadslist, makethreadlistdata($data);
	unshift @threadslist, ($number+1)."\n";
	savethreadslist(@threadslist);

	# スレのファイルを作る
	savethread($number,$thread);
	chmod $ini::filePermission, "$ini::data/$number.cgi";

	fileunlock();

	# 返信処理してもらう
	unless(reply($number,$cgi)){
		#失敗
		return -1;
	}
	return $number;
}
# スレを消す処理
sub thdelete{
	my($number)=shift;
	unless(testthread($number)){
		return 1;
	}
	unless(filelock()){
		return 1;
	}
	my(@threadslist)=loadthreadslist();
	my($th_number)=shift @threadslist;
	my($thread)=loadthread($number);
	my($i)=0;
	my($waste)={
		'number' =>$number,
		'title'=>$thread->{'title'},
		'date' =>time_str(),
		'etc' =>'管理人による削除',
		'seen'=>$thread->{'seen'}
	};
	foreach(@threadslist){
		if($_ =~ /^$number\t/){
			splice @threadslist,$i,1;
			last;
		}
		$i++;
	}
	unless(open(FILE,">>$ini::data/waste.cgi")){
		return 0;
	}
	my($d)=makewastelistdata($waste);
	chomp $d;
	print FILE "$d\n";
	close(FILE);
	unshift @threadslist,$th_number;
	savethreadslist(@threadslist);
	$thread->{'alive'}=0;
	savethread($number,$thread);
	fileunlock();
	return 0;

}
# スレを復活させる処理
sub threstore{
	my($number)=shift;
	unless(testthread($number)){
		return 1;
	}
	unless(filelock()){
		return 1;
	}
	my(@threadslist)=loadthreadslist();
	my($th_number)=shift @threadslist;
	my($thread)=loadthread($number);

	my($reses)=$thread->{'res'};
	my($date)=${$reses}[0]->{'date'};
	if($date =~ /;(.+?)$/){
		$date=$1;
	}
	my($date2)=${$reses}[$#{$reses}]->{'date'};
	if($date2 =~ /;(.+?)$/){
		$date2=$1;
	}
	my($thlistdata)={
		'number' =>$number,
		'title'=>$thread->{'title'},
		'maker'=>$thread->{'maker'},
		'mdate'=>$date,
		'date'=>$date2,
		'lastreply'=>${$reses}[$#{$reses}]->{'name'},
		'resnum'=>scalar grep{$_->{'flag'}==0}(@{$reses}),
		'seen'=>0
	};
	unshift @threadslist,makethreadlistdata($thlistdata);
	unless(open(FILE,"$ini::data/waste.cgi")){
		return 0;
	}
	my(@waste)=<FILE>;
	close(FILE);
	my($i)=0;
	foreach(@waste){
		if($_ =~ /^$number\t/){
			splice @waste,$i,1;
		}
		$i++;
	}
	open(FILE,">$ini::data/waste.cgi");
	foreach(@waste){
		chomp;
		print FILE "$_\n";
	}
	close(FILE);

	unshift @threadslist,$th_number;
	
	savethreadslist(@threadslist);
	$thread->{'alive'}=1;
	savethread($number,$thread);
	fileunlock();
	return 0;

}

# 返信データが不正でないかチェック
# 0:正常 1:入力漏れ 2:禁止ワード
sub testreplydata{
	my($cgi)=shift;
	return 1 if(($cgi->param('name') eq "")&&($ini::noName eq ""));
	return 1 if($cgi->param('title') eq "");
	return 1 if($cgi->param('message') eq "");
	return 1 if(($cgi->param('password') eq "")&&($ini::noPassword==0));
	if(-e "$ini::data/kinsi.cgi"){
		if(open(FILE, "$ini::data/kinsi.cgi")){
			while(<FILE>){
				chomp;
				if($cgi->param('message') =~ /$_/){
					close(FILE);
					return 2;
				}
			}
			close(FILE);
		}
	}
	return 0;
}

# 検索
sub find{
	my($cgi)=shift;
	my($mode)=$cgi->param('searchmode');
	my(@words) = split(/\s+/,safevalue($cgi->param('search')));
	my(@checklist)=$cgi->param('in');

	output::find_header();

	my(@threadslist)=loadthreadslist();
	shift @threadslist;
	my($num)=0;	# 検索済み件数

OUTLOOP:foreach(@threadslist){
		my($tt_flg)=0;
		my($number)=split(/\t/);

		my($thread)=loadthread(int($number));
		#チェック
		my($che,$re,$wo);
		foreach $re(@{$thread->{'res'}}){
			next if($re->{'flag'}!=0);
			my($flg)=($mode eq "and" ? 1 : 0);
			INLOOP:foreach $wo(@words){
				my($fflg)=0;
				foreach $che(@checklist){
					if($re->{$che} =~ /$wo/){
						$fflg=1;
						if($mode ne "and"){
							$flg=1;
							last INLOOP;
						}
					}
				}
				if($mode eq "and"){
					if($fflg==0){
						$flg=0;
						last;
					}
				}
			}
			next if($flg==0);
			# 条件にマッチ
			if($tt_flg==0){
				output::find_label(int($number),$thread->{'title'});
				$tt_flg=1;
			}
			output::res($re,\@words,$number);
			$num++;
			last OUTLOOP if($num >= $ini::search_max);

		}
	}
	if($num==0){
		# 見つからない
		print <<END;
<p>1件も見つかりませんでした。</p>
END
	}else{
		print <<END;
<p><b>$num件</b>見つかりました。</p>
END
	}
	output::find_footer();
}







#----------------------------------------------------------------------------
# 名前の加工
sub getname{
	my($name)=shift;
	if($name eq ""){
		$name=$ini::noName;
	}
	return safevalue($name);
}
# 表示するときの名前
sub showname{
	my($name)=shift;
	if($ini::use_trip!=0){
		$name =~ s/◆/◇/g;
		if($name =~ /\#(.+)/){
			my($k)=$1;
			$name =~ s/\#.+//;
			my($salt)=substr($k."H.",1,2);
			$salt=~ s/[^\.-z]/\./go;
			$salt =~ tr/:;<=>?@[\\]^_`/ABCDEFGabcdef/;
			my($trip) = substr( crypt($k,$salt), -10);
			$name .= "◆$trip";
		}
	}
	return $name;
}
# 安全化
sub safevalue{
	my($value)=shift;
	$value=~s/&/&amp;/g;
	$value=~s/</&lt;/g;
	$value=~s/>/&gt;/g;
	return $value;
}
# 正規表現の安全化
sub saferegexp{
	my($value)=shift;
	$value=~s/([\x20-\x2F\x3C-\x40\x5B-\x60\x7B-\x7E])/\\$1/g;
	return $value;
}
# パスワードチェック
sub checkpassword{
	my($ans,$inp)=@_;
	return 1 if(($ans eq $inp)||($inp eq $ini::password));
	return 0;
}
# 時間を文字列で得る
sub time_str{
	my($sec,$min,$hour,$day,$mon,$year,$wday)=localtime(time);
	return sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",$year+1900,$mon+1,$day,
	("日","月","火","水","木","金","土")[$wday], $hour, $min, $sec);
}
# アク禁設定
sub akukincheck{
	return 0 unless(-e "$ini::data/akukin.cgi");
	return 0 unless(open(FILE,"$ini::data/akukin.cgi"));
	my(@lines)=<FILE>;
	close(FILE);
	foreach(@lines){
		chomp;
		if($_ =~ /^\d+\.\d+\.\d+\.\d+$/){
			return 1 if($ENV{'REMOTE_ADDR'} eq $_);
		}elsif($_ =~ /^(\d+\.\d+\.\d+\.\d+)\/(\d+)$/){
			my($ips) = makeipnumber($1);
			my($nip) = makeipnumber($ENV{'REMOTE_ADDR'});
			my($m)=32-int($2);
			my($mask)=0xFFFFFFFF;
			for(my($i)=0;$i<$m;$i++){
				$mask ^= 1<<$i;
			}
			return 1 if(($ips&$mask)==($nip&$mask));
		}
	}
	return 0;
}
sub makeipnumber{
	my($ip)=shift;
	my(@ips)=split(/\./,$ip);
	return (int($ips[0])<<24) | (int($ips[1])<<16) | (int($ips[2])<<8) | int($ips[3]);
}






return 1;
