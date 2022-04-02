package output;
#output:出力パッケージ

# 外部から呼び出されるサブルーチン

# ヘッダ
sub topheader{
	cookie_header();
	print <<END;
Content-type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<title>$ini::bbsName</title>
<link rel="stylesheet" type="text/css" href="style.css" />
<script type="text/javascript" src="script.js"></script>
</head>
<body>
<header id="header">
<hgroup>
<h1>$ini::bbsName</h1>
<h2>$ini::bbsDescription</h2>
</hgroup>
END
	navi();
	print <<END;
</header>
END
}

# スレッド一覧のヘッダ
sub threads_header{
	print <<END;
<article id="threads">
<h2>スレッド一覧</h2>
END
}
# スレッド一覧テーブルのヘッダ
sub threads_table_header{
	my($page,$threads_number)=@_;


	threads_header();
	if($page>=0){
		threads_navi($page,$threads_number,'up');
	}
	print <<END;
<table>
<tr>
<th>No</th><th>題名</th><th>レス数</th><th>参照数</th><th>作成</th><th>最終更新</th>
</tr>

END
}
# スレッド一覧のページ
sub threads_navi{
	my($page,$threads_number,$mode)=@_;
	print <<END;
<nav class="pager $mode">
END
	my($i);
	for($i=0;$i<$threads_number/$ini::page_threads;$i++){

		print "<a";
		if($i*$ini::page_threads==$page){
			print " class='current'";
		}
		print " href='index.cgi?page=".($i*$ini::page_threads)."'>$i</a>\n";
	}
	print <<END;
</nav>
END
}
# 1つのスレッド
sub threads_thread{
	my($data)=@_;
	my($number)=$data->{'number'};
	my($res)=$data->{'resnum'}-1;#レス数は投稿の数より1少ない
	my($href);
	if($::Global_admin_mode==1){
		$href="admin.cgi?mode=administer&number=$number&password=$ini::password";
	}else{
		$href="index.cgi?mode=view&number=$number";
	}
	my($maker)=data::showname($data->{'maker'});
	my($lastreply)=data::showname($data->{'lastreply'});
	print <<END;
<tr>
<td class="number">$number</td><td><a href="$href">$data->{'title'}</a></td>
<td class="number">$res</td><td class="number">$data->{'seen'}</td>
<td>$maker<br>$data->{'mdate'}</td>
<td>$lastreply<br>$data->{'date'}</td>
</tr>
END
}
# スレッド一覧テーブルのフッタ
sub threads_table_footer{
	my($page,$threads_number)=@_;
	print <<END;
</table>
END
	if($page>=0){
		threads_navi($page,$threads_number,'down');
	}
	threads_footer();
}
# スレッド一覧のフッタ
sub threads_footer{
	print <<END;
</article>
END
}

#フッタ
sub footer{
	# 広告は削除しないようにして下さい。
	my($admin)="admin.cgi";
	if($::Global_admin_mode==1){
		$admin.="?password=$ini::password&mode=login";
	}
	print <<END;
<footer id="footer">
<p><a href="https://github.com/noty2008">noty2008</a>作の高機能掲示板 0.6</p>
<p style="text-align:right">[<a href="$admin">管理者ページ</a>]</p>
</footer>
</body>
</html>
END
}
#============================================================

# 記事のヘッダ
sub view_header{
	my($data)=shift;
	my($title)=$data->{'title'};
	my($number)=$data->{'number'};
	print <<END;
Content-type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<title>$ini::bbsName - $title</title>
<link rel="stylesheet" type="text/css" href="style.css" />
<script type="text/javascript" src="script.js"></script>
</head>
<body>
<header id="header">
<hgroup>
<h1>$ini::bbsName</h1>
<h2>$ini::bbsDescription</h2>
</hgroup>
END
	navi();
	print <<END;
</header>
END
	if($::Global_admin_mode==1){
		print <<END;
<p><a href="admin.cgi?mode=administer&password=$ini::password">戻る</a></p>
END
	}
	view_article($data);
}
sub view_article{
	my($data)=@_;
	my($number,$title)=($data->{'number'},$data->{'title'});
	print <<END;
<article class="view">
<h2><a href="index.cgi?mode=view&number=$number">$title</a></h2>
END
}
# 記事のフッタ
sub view_footer{
	print <<END;
</article>
END
}
# レス1つ
sub res{
	my($data,$words,$number)=@_;
	my($cl) = $data->{'num'}==1 ? "res top" : "res";

	my($title,$name,$message,$date,$date_r,$color)=($data->{'title'},$data->{'name'},$data->{'message'},$data->{'date'},$data->{'date2'},$data->{'color'});
	$name = data::showname($name);
	if($words){
		foreach(@$words){
			my($p)=data::saferegexp($_);

			$title =~ s/((?:$p)+)/<mark>$1<\/mark>/g;
			$name =~ s/((?:$p)+)/<mark>$1<\/mark>/g;
			$message =~ s/((?:$p)+)/<mark>$1<\/mark>/g;

		}
	}
	if($ini::use_email==1){
		my($em)=$data->{'email'};
		if($em ne ""){
			$name = '<a href="mailto:'.$em.'">'.$name.'</a>';
		}
	}
	my($c_style)="";
	if($color =~ /^\s*(#[0-9a-fA-F]{6})\s*$/){
		$c_style=' style="color:'.$1.'"';
	}

	my($ddd)="";
	if($ini::use_URL==1){
		my($url)=$data->{'url'};
		if($url ne ""){
			$ddd.=' <a href="'.$url.'" target="_blank">URL</a>';
		}
	}
	if($::Global_admin_mode==1){
		$date=~ s/;.*//;
		$ddd=" IPアドレス:<b class='ip'>$data->{'ip'}</b>";
	}
	# time要素用の加工
	my($sec,$min,$hour,$da,$month,$year)=localtime(int($date_r));
	my($date2)=sprintf("%d-%02d-%02dT%02d:%02d:%02d%s",$year+1900,$month+1,$da,$hour,$min,$sec,$ini::timezone);

	if(($data->{'flag'}==1)||($data->{'flag'}==2)){
		$cl .= " deleted";
	}

	# メッセージ加工
	$message =~ s/\n/<br>\n/g;
	my($url_pattern) = 'https?://[A-Za-z0-9\-.!~*' . "'" . '()/?;$&@=+,#%]+';
	$message =~ s/($url_pattern)/<a href="$1">$1<\/a>/g;

	$message =~ s/&gt;&gt;([0-9\-]+)/<a href="index.cgi?mode=view&number=$number&res=$1">&gt;&gt;$1<\/a>/g;

	print <<END;
<article class="$cl">
<header>
<h3 class="title">$title</h3>
<p>$data->{'num'}. <b class="name">$name</b> <time datetime="$date2" pubdate>$date</time>$ddd</p>
</header>
<p$c_style>$message</p>
</article>
END
}
# 返信フォーム
sub view_reply{
	my($number,$data,$cgi)=@_;
	my($name,$password)=($cgi->cookie("bbs_name"), $cgi->cookie("bbs_password"));
	my($url,$email)=($cgi->cookie("bbs_url"), $cgi->cookie("bbs_email"));
	my($color)=$cgi->cookie("bbs_color");
	replydata_form({
		'name' => $name,
		'password' => $password,
		'title' => $data->{'title'},
		'message' => "",
		'url' => $url,
		'email' => $email,
		'color' => $color
	},"返信フォーム","reply",<<END);
<input type="hidden" name="number" value="$number" />
<input type="hidden" name="mode" value="reply" />
END
}
sub replydata_form{
	my($initdata,$formtitle,$formid,$option)=@_;
	my($name,$password,$title,$message,$url,$email,$color);
	if($initdata){
		($name,$password,$title,$message,$url,$email,$color) =
		($initdata->{'name'},$initdata->{'password'},$initdata->{'title'},$initdata->{'message'},$initdata->{'url'},$initdata->{'email'},$initdata->{'color'});
	}
	my($password_req)=$ini::noPassword==1 ? "" : " required";
	my($noname_req)=$ini::noName eq "" ? " required" : "";

	my(@c_name)=();
	my(@c_value)=();
	if($ini::use_color==1){
		# 色一覧
		my($l_number)=0;
		if(open(FILE,"$ini::data/colorlist.cgi")){
			while(<FILE>){
				chomp;
				($c_name[$l_number],$c_value[$l_number])=split(/\t/);
				$l_number++;
			}
			close(FILE);
		}
		if($l_number==0){
			# 色が無い
			@c_name=("黒");
			@c_value=("#000000");
		}
	}

	print <<END;
<article id="$formid" class="form">
<h2>$formtitle</h2>
<form action="index.cgi" method="post" id="replyform">
$option
<p><b>名前:</b>
<input type="text" size="30" name="name" value="$name"$noname_req />
</p>
<p>
<b>題名:</b>
<input type="text" size="50" name="title" value="$title" required />
</p>
END
	if($ini::use_URL==1){
		print <<END;
<p>
<b>URL:</b>
<input type="url" size="50" name="url" value="$url" />
</p>
END
	}else{
		print <<END;
<input type="hidden" name="url" value="" />
END
	}
	if($ini::use_email==1){
		print <<END;
<p>
<b>メール:</b>
<input type="email" size="50" name="email" value="$email" />
</p>
END
	}else{
		print <<END;
<input type="hidden" name="email" value="" />
END
	}
	print <<END;
<p>
<b>内容:</b>
<textarea cols="50" rows="6" name="message" required>
$message</textarea>
</p>
END
	if($ini::use_color==1){
		print <<END;
<p>
<b>色:</b>
END
		for(my($i)=0;$i<@c_name;$i++){
			my($cn)=$c_name[$i];
			my($cv)=$c_value[$i];

			my($ch)= $cv eq $color ? " checked" : "";

			print <<END;
<label style="color:$cv"><input type="radio" name="color" value="$cv"$ch /><span class="colorchip" title="$cv">$cn</span></label>
END
		}
		print "</p>\n";
	}elsif($ini::use_color==2){
		print <<END;
<p>
<b>色:</b>
END
#		if($color !~ /^\s*#[0-9a-fA-F]{6}\s*$/){
#			$color="";
#		}
		print <<END;
<input type="color" name="color" value="$color" /></p>
END
	}
	print <<END;
<p>
<b>パスワード:</b>
<input type="password" name="password" size="15" value="$password"$password_req />
<input type="submit" value="送信" /></p>
<p id="error_message"></p>
</form>
</article>
<script type="text/javascript">
var noPassword = $ini::noPassword;
var noName = "$ini::noName";

var form = document.getElementById('replyform');
if(form){
	if(form.addEventListener){
		form.addEventListener('submit',check_input,false);
	}else if(form.attachEvent){
		form.attachEvent('onsubmit',check_input);
	}
}
</script>
END
}
# ページャー
sub view_navi{
	my($number,$page,$res_number,$mode)=@_;
	return if($res_number<=$ini::page_res);
	print <<END;
<nav class="pager $mode">
END
	my($i);
	for($i=0;$i<$res_number/$ini::page_res;$i++){

		print "<a";
		if($i*$ini::page_res==$page){
			print " class='current'";
		}
		print " href='index.cgi?mode=view&number=$number&page=".($i*$ini::page_res)."'>$i</a>\n";
	}
	print <<END;
</nav>
END
}
# 削除フォーム
sub view_delete{
	my($number)=shift;
	my($adminstr)="";
	if($::Global_admin_mode==1){
		$adminstr = <<END;
<input type="hidden" name="adminmode" value="adminmode" />
END
	}
	print <<END;
<article id="delete" class="form">
<h2>記事の編集・削除</h2>
<form action="index.cgi" method="post">
<input type="hidden" name="number" value="$number" />$adminstr
<p><b>レス番号:</b>
<input type="text" size="20" name="res_number" />
</p>
<p>
<b>パスワード:</b>
<input type="password" size="20" name="password" />
</p>
<p>
<b>
<select name="mode">
<option value="delete" selected>削除</option>
<option value="edit">編集</option>
</select>
</b>
<input type="submit" value="送信" /></p>
</form>
</article>
END
}
# スレ削除フォーム
sub view_thdelete{
	my($number)=shift;
	print <<END;
<article id="delete" class="form">
<h2>スレッドの削除</h2>
<form action="admin.cgi" method="post">
<p><input type="hidden" name="number" value="$number" />
<input type="hidden" name="mode" value="thdelete" />
<input type="hidden" name="password" value="$ini::password" />
<input type="submit" value="削除" /></p>
</form>
</article>
END
}
# スレ復活フォーム
sub view_threstore{
	my($number)=shift;
	print <<END;
<article id="delete" class="form">
<h2>スレッドの復活</h2>
<form action="admin.cgi" method="post">
<p><input type="hidden" name="number" value="$number" />
<input type="hidden" name="mode" value="threstore" />
<input type="hidden" name="password" value="$ini::password" />
<input type="submit" value="復活" /></p>
</form>
</article>
END
}
# レス編集ページ
sub editres{
	my($number,$res_number,$thread,$res,$old_password)=@_;
	view_header($thread);
	res($res,undef,$number);
	view_footer();

	$res->{'message'} =~ s/\<.+\>//g;

	my($formstr) = <<END;
<input type="hidden" name="mode" value="edit_do" />
<input type="hidden" name="number" value="$number" />
<input type="hidden" name="res_number" value="$res_number" />
<input type="hidden" name="old_password" value="$old_password" />
END
	if($::Global_admin_mode==1){
		$formstr .= <<END;
<input type="hidden" name="adminmode" value="adminmode" />
<input type="hidden" name="masterpassword" value="$ini::password" />
END
	}
	replydata_form($res,"レス編集フォーム","resedit",$formstr);
}

#=====================================================
#新スレのページ
sub newpage{
	my($cgi)=shift;
	my($name,$password)=($cgi->cookie("bbs_name"), $cgi->cookie("bbs_password"));
	my($url,$email)=($cgi->cookie("bbs_url"), $cgi->cookie("bbs_email"));
	my($color)=$cgi->cookie("bbs_color");
	topheader();
	replydata_form({
		'name' => $name,
		'password' => $password,
		'title' => "",
		'message' => "",
		'url' => $url,
		'email' => $email,
		'color' => $color
	},"新規スレッド作成","new",<<END);
<input type="hidden" name="mode" value="newdo" />
END
	footer();
	return;
}
#=====================================================
sub searchpage{
	topheader();
	print <<END;
<article class="form">
<h2>検索</h2>
<form action="index.cgi" method="post">
<p><input type="hidden" name="mode" value="find" />
<b>モード:</b>
<label><input type="radio" name="searchmode" value="or" checked="checked" />OR検索</label>　
<label><input type="radio" name="searchmode" value="and" />AND検索</label>
</p>
<p><input type="hidden" name="mode" value="find" />
<b>検索対象:</b>
<label><input type="checkbox" name="in" value="name" />名前</label>　
<label><input type="checkbox" name="in" value="title" />タイトル</label>　
<label><input type="checkbox" name="in" value="message" checked="checked" />本文</label>　
</p>
<p>
<b>検索語句:</b>
<input type="text" size="40" name="search" />
</p>
<p>
<b></b>
<input type="submit" value="検索" /></p>
</form>
</article>
END
	footer();
}
sub find_header{
	topheader();
	print <<END;
<article id="find">
<h2>検索結果</h2>
END
}
#スレッドごと
sub find_label{
	my($number,$title)=@_;
	print <<END;
<h3><a href="index.cgi?mode=view&number=$number">$title</a></h3>
END
}
sub find_footer{
	print <<END;
</article>
END
	footer();
}

#=====================================================
#cookieのHTTPヘッダ
sub cookie_header{
	my($cgi)=$::cgi;
	my(@list)=();
	if($::mode =~ /^(?:reply|newdo|edit_do)$/){
		push @list,('name','title','password','top');
		if($ini::use_URL==1){
			push @list,'url';
		}
		if($ini::use_email==1){
			push @list,'email';
		}
		if($ini::use_color>0){
			push @list,'color';
		}
	}
	foreach(@list){
		my($val)=$cgi->param($_);
		my($cookie) = $cgi->cookie(-name => "bbs_$_",
			-value => $val,
			-expires => ($val ? "+30d" : "-1d"));
		$cookie =~ s/path\s*=\s*[^;]*;//i;
		print "Set-Cookie: $cookie\n";
	}
}



#=====================================================

# エラー（全部出力）
sub error1{
	topheader();
	error2($_[0]);
	footer();
}
# エラー（エラー部分だけ出力）
sub error2{
	print <<END;
<article class="error">
<p><strong>エラー</strong>：$_[0]</p>
</article>
END
}
#-----------------
# 内部で使うサブルーチン
sub navi{
	print <<END;
<nav>
  <ul>
    <li><a href="$ini::site">サイトに戻る</a></li>
    <li><a href="index.cgi">掲示板ホーム</a></li>
    <li><a href="index.cgi?top=table">スレッド表示</a></li>
    <li><a href="index.cgi?top=open">リスト表示</a></li>
    <li><a href="index.cgi?mode=new">新規スレッド作成</a></li>
    <li><a href="index.cgi?mode=search">検索</a></li>
  </ul>
</nav>
END
}








return 1;
