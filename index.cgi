#! /usr/local/bin/perl

# 高機能掲示板 v0.6

require "ini.cgi";
require "output.cgi";
require "data.cgi";
use CGI;

$cgi = new CGI;

$mode = $cgi->param('mode');

# トップの表示モード
$top_mode = $cgi->cookie("bbs_top");
if(!$top_mode){
	$top_mode="table";
}
$a_top=$cgi->param('top');
if($a_top eq "table" || $a_top eq "open"){
	$top_mode=$a_top;
}

$Global_admin_mode = 0;

if($ini::use_akukin==2){
	if(data::akukincheck()==1){
		akukin();
		exit(0);
	}
}


if($mode eq ''){
	output::topheader();
	threads();
	output::footer();
}elsif($mode eq 'view'){
	# 見る
	view(int($cgi->param('number')));
}elsif($mode eq 'search'){
	# 検索ページ
	searchpage();
}elsif($mode eq 'find'){
	# 検索結果
	find();
}else{
	# アク禁設定
	if($ini::use_akukin==1){
		if(data::akukincheck()==1){
			akukin();
			exit(0);
		}
	}
	if($mode eq 'reply'){
		# 返信
		reply();
	}elsif($mode eq 'new'){
		# 新スレ
		newpage();
	}elsif($mode eq 'newdo'){
		# 新スレ作成
		newthread();
	}elsif($mode eq 'delete'){
		# レスを消す
		deleteres();
	}elsif($mode eq 'edit'){
		# レスを編集
		editres();
	}elsif($mode eq 'edit_do'){
		# レスを編集実行
		editres_do();
	}else{
		output::topheader();
		threads();
		output::footer();
	}
}




# スレッド一覧
sub threads{
	my($page)=int($cgi->param('page'));
	$page=0 if($page<0);

	data::threads_table($page);

}
# 記事
sub view{
	$number = shift;
	data::view($number,int($cgi->param('page')),$cgi,"normal");
}
# 返信
sub reply{
	# 返信処理
	unless(data::reply($cgi->param('number'),$cgi)){
		# 失敗したならそのまま終了
		return;
	}
#	print "Location: $ENV{'SCRIPT_NAME'}?mode=view&number=" . $cgi->param('number'). "\n";
	output::cookie_header($cgi);
#	print "\n\n";
#	output::cookie_header($cgi);
	view($cgi->param('number'));
#	output::cookie_header($cgi);
}
#新スレ
sub newpage{
	output::newpage($cgi);
}
sub newthread{
	my($number)=data::newthread($cgi);
	if($number<0){
		#エラーがあった
		return;
	}

	print "Location: $ENV{'SCRIPT_NAME'}?mode=view&number=" . $number. "\n";
	output::cookie_header($cgi);
	print "\n";
}

sub searchpage{
	output::searchpage();
}
sub find{
	data::find($cgi);
}
sub deleteres{
	if($ini::delete_free==0){
		if($cgi->param('password') ne $ini::password || $cgi->param('adminmode') ne "adminmode"){
			output::topheader();
			threads();
			output::footer();
			return;
		}
	}
	if(data::deleteres($cgi)){
		view(int($cgi->param('number')));
	}
}
sub editres{
	if($ini::delete_free==0){
		if($cgi->param('password') ne $ini::password || $cgi->param('adminmode') ne "adminmode"){
			output::topheader();
			threads();
			output::footer();
			return;
		}else{
			$::Global_admin_mode=1;
		}
	}
	data::editres_init($cgi);
}
sub editres_do{
	if($ini::delete_free==0){
		if($cgi->param('masterpassword') ne $ini::password || $cgi->param('adminmode') ne "adminmode"){
			output::topheader();
			threads();
			output::footer();
			return;
		}
	}
	if(data::editres_do($cgi)){
		view(int($cgi->param('number')));
	}
}
sub akukin{
	output::error1("アクセス禁止のため、利用することができません。");
}
