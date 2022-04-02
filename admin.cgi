#! /usr/local/bin/perl

require "ini.cgi";
require "data.cgi";
require "output.cgi";

use CGI;

$cgi = new CGI;

if($cgi->param('mode') eq 'administer'){
	
	unless($cgi->param('password') eq $ini::password){
		print <<END;
Content-type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<title>管理者ページ</title>
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
<header id="header">
<h1>管理者ページ</h1>
</header>
<article>
<h2>管理者モード</h2>
<p><strong>エラー</strong>：パスワードが違います。</p>
</article>
</body>
</html>
END
		exit(0);
	}
	administer();
	exit(0);
}

print <<END;
Content-type: text/html; charset=UTF-8

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8" />
<title>管理者ページ</title>
<link rel="stylesheet" type="text/css" href="style.css" />
<style type="text/css">
.form b{
	width:15em;
}
</style>
</head>
<body>
<header id="header">
<h1>管理者ページ</h1>
</header>
<p><a href="index.cgi">掲示板に戻る</a></p>
END
if(!(-e $ini::data) || $cgi->param('mode') eq 'init2'){
	# データディレクトリが無い
	if($cgi->param('mode') eq 'init2'){
		unless($cgi->param('password') eq $ini::password){
			loging();
			exit(0);
		}
	}
	if($cgi->param('mode') eq 'init' || $cgi->param('mode') eq 'init2'){
		# 初期化
		print <<END;
	<article>
	<h2>初期設定</h2>
END
		if($cgi->param('mode') eq 'init'){
			if(init_ini()==0){
				print <<END;
<p><strong>エラー</strong>が発生しました。正常に初期化できませんでした。</p>
<p><a href="admin.cgi?mode=login&password=$ini::password">戻る</a></p>
</article>
</body>
</html>
END
				return;
			}
			$ini::data=$cgi->param('data');
		}
		my($result) = data::init();
		if($result==0){
			print <<END;
<p>初期化を完了しました。掲示板が利用可能な状態になりました。</p>
<p><a href="index.cgi">掲示板に入る</a>｜<a href="admin.cgi?mode=login&password=$ini::password">管理者ページに戻る</a></p>
</article>
</body>
</html>
END
		}else{
			print <<END;
<p><strong>エラー</strong>が発生しました。正常に初期化できませんでした。</p>
<p><a href="admin.cgi?mode=login&password=$ini::password">戻る</a></p>
</article>
</body>
</html>
END
		}
	exit(0);
	}

	print <<END;
<article>
<h1>初期設定</h1>
<form action="admin.cgi" method="post">
<p>必要な情報を入力して下さい。</p>
<h2>パスワード</h2>
<p>パスワード：<input type="text" name="newpassword" value="$ini::password" size="30" /></p>
<p>パスワードは、後から管理画面で変更可能です。</p>
<h2>ディレクトリ</h2>
<p>データを保存するディレクトリ：<input type="text" name="data" value="$ini::data" size="20" /></p>
<p>この設定は、掲示板のデータを保存しておくディレクトリを指定するものです。他の人に分からないような名前にして下さい。</p>
<p>この設定は、今後は<strong>管理画面からは変更できません</strong>。</p>

<h2>掲示板の初期化</h2>
<p>掲示板を初期化して、使用できるようにします。</p>
<p>
<input type="hidden" name="mode" value="init" />
<input type="submit" value="初期化" />
</p>
</form>
</article>
</body>
</html>
END
	exit(0);
}
unless($cgi->param('password') eq $ini::password){
	loging();
	exit(0);
}

if($cgi->param('mode') eq 'restore'){
	# 復旧
		print <<END;
<article>
<h2>復旧</h2>
END
	my($result) = data::restore();
	if($result==0){
		print <<END;
<p>復旧を完了しました。</p>
<p><a href="index.cgi">掲示板に入る</a>｜<a href="admin.cgi?mode=login&password=$ini::password">管理者ページに戻る</a></p>
</article>
</body>
</html>
END
	}else{
		print <<END;
<p><strong>エラー</strong>が発生しました。正常に復旧できませんでした。</p>
<p><a href="admin.cgi?mode=login&password=$ini::password">戻る</a></p>
</article>
</body>
</html>
END
	}
exit(0);
}
if($cgi->param('mode') eq 'thdelete'){
	# スレ削除
		print <<END;
<article>
<h2>スレ削除</h2>
END
	my($result) = data::thdelete(int($cgi->param('number')));
	if($result==0){
		print <<END;
<p>削除を完了しました。</p>
<p><a href="index.cgi">掲示板に入る</a>｜<a href="admin.cgi?mode=login&password=$ini::password">管理者ページに戻る</a></p>
</article>
</body>
</html>
END
	}else{
		print <<END;
<p><strong>エラー</strong>が発生しました。正常に削除できませんでした。</p>
<p><a href="admin.cgi?mode=login&password=$ini::password">戻る</a></p>
</article>
</body>
</html>
END
	}
exit(0);
}
if($cgi->param('mode') eq 'threstore'){
	# スレ復活
		print <<END;
<article>
<h2>スレッドの復活</h2>
END
	my($result) = data::threstore(int($cgi->param('number')));
	if($result==0){
		print <<END;
<p>スレッドの復活を完了しました。</p>
<p><a href="index.cgi">掲示板に入る</a>｜<a href="admin.cgi?mode=login&password=$ini::password">管理者ページに戻る</a></p>
</article>
</body>
</html>
END
	}else{
		print <<END;
<p><strong>エラー</strong>が発生しました。正常に復活できませんでした。</p>
<p><a href="admin.cgi?mode=login&password=$ini::password">戻る</a></p>
</article>
</body>
</html>
END
	}
exit(0);
}

if($cgi->param('mode') eq 'delview'){
	# 表示
	print <<END;
<article id="threads">
<h2>削除されたスレッド一覧</h2>
<table>
<tr>
<th>No</th><th>題名</th><th>削除日時</th><th>備考</th>
</tr>
END
	open(FILE,"$ini::data/waste.cgi");
	my(@wastes)=<FILE>;
	close(FILE);
	foreach(@wastes){
		my($waste)=data::getwastelistdata($_);
		print <<END;
<tr><td>$waste->{'number'}</td><td><a href="admin.cgi?mode=administer&number=$waste->{'number'}&password=$ini::password">$waste->{'title'}</a></td>
<td><time>$waste->{'date'}</time></td><td>$waste->{'etc'}</td></tr>
END
	}
	print "</table>\n";
	print "<p>削除されたスレッドは<b>".(scalar @wastes)."個</b>あります。</p>\n";
	print <<END;
</article>
</body>
</html>
END
	exit(0);
}
if($cgi->param('mode') eq 'change'){
	# 設置一覧
	change();
	exit(0);
}
if($cgi->param('mode') eq 'changeini'){
	# 設置一覧変更
	changeini();
	exit(0);
}
if($cgi->param('mode') eq 'akukin'){
	# アク禁設定
	akukin();
	exit(0);
}
if($cgi->param('mode') eq 'changeakukin'){
	# アク禁設定
	changeakukin();
	exit(0);
}
if($cgi->param('mode') eq 'style'){
	# スタイル設定
	style();
	exit(0);
}

if($cgi->param('mode') eq 'changestyle'){
	# スタイル変更
	changestyle();
	exit(0);
}
if($cgi->param('mode') eq 'kinsi'){
	# 禁止ワード設定
	kinsi();
	exit(0);
}
if($cgi->param('mode') eq 'changekinsi'){
	# 禁止ワード変更
	changekinsi();
	exit(0);
}
if($cgi->param('mode') eq 'colorlist'){
	# 使用色設定
	colorlist();
	exit(0);
}
if($cgi->param('mode') eq 'changecolorlist'){
	# 使用色変更
	changecolorlist();
	exit(0);
}

	if($cgi->param('mode') eq ''){
		# ログイン前
		loging();
		exit(0);
	}
	# ログイン後

	print <<END;
<article>
<h1>管理画面</h1>
END
	if(data::test()==0){
		print <<END;
<p><strong>ファイルに異常が発生しています。</strong></p>
END
		if(!(-e "$ini::data/threads.cgi")&&(-e "$ini::data/waste.cgi")){
			print <<END;
<p><b>threads.cgi</b>がありません。今あるファイルを利用して<b>threads.cgi</b>を復旧できる可能性があります。</p>
END
		}elsif((-e "$ini::data/threads.cgi")&& !(-e "$ini::data/waste.cgi")){
			print <<END;
<p><b>waste.cgi</b>がありません。今あるファイルを利用して<b>waste.cgi</b>を復旧できる可能性があります。</p>
END
		}elsif(!(-e "$ini::data/threads.cgi")&& !(-e "$ini::data/waste.cgi")){
			print <<END;
<p><b>threads.cgi</b>と<b>waste.cgi</b>がありません。今あるファイルを利用して復旧できる可能性があります。</p>
END
		}
		print <<END;
<form action="admin.cgi" method="post">
<p>
<input type="hidden" name="password" value="$ini::password" />
<input type="hidden" name="mode" value="restore" />
<input type="submit" value="復旧する" />
</p>
</form>
END
	}
	print <<END;
<h2>管理者モード</h2>
<p>管理者モードで掲示板を閲覧すると、削除された書き込みや、編集された書き込みの編集前の状態を確認することができます。</p>
<p>また、書き込み時のIPアドレスを閲覧できます。</p>
<form action="admin.cgi" method="post">
<p>
<input type="hidden" name="password" value="$ini::password" />
<input type="hidden" name="mode" value="administer" />
<input type="submit" value="管理者モード"/>
</p>
</form>
<form action="admin.cgi" method="post">
<p>
<input type="hidden" name="password" value="$ini::password" />
<input type="hidden" name="mode" value="delview" />
<input type="submit" value="削除したスレッドを見る" />
</p>
</form>

<h2>設定の変更</h2>
<p>現在の掲示板の設定を変更できます。</p>
<form action="admin.cgi" method="post">
<p>
<input type="hidden" name="password" value="$ini::password" />
<input type="hidden" name="mode" value="change" />
<input type="submit" value="設定変更画面" />
</p>
</form>
<form action="admin.cgi" method="post">
<p>
<input type="hidden" name="password" value="$ini::password" />
<input type="hidden" name="mode" value="style" />
<input type="submit" value="スタイル変更画面" />
</p>
</form>
<form action="admin.cgi" method="post">
<p>
<input type="hidden" name="password" value="$ini::password" />
<input type="hidden" name="mode" value="kinsi" />
<input type="submit" value="禁止ワード設定画面" />
</p>
</form>
END
	if($ini::use_akukin!=0){
		print <<END;
<form action="admin.cgi" method="post">
<p>
<input type="hidden" name="password" value="$ini::password" />
<input type="hidden" name="mode" value="akukin" />
<input type="submit" value="アクセス禁止設定画面" />
</p>
</form>
END
	}
	if($ini::use_color==1){
		print <<END;
<form action="admin.cgi" method="post">
<p>
<input type="hidden" name="password" value="$ini::password" />
<input type="hidden" name="mode" value="colorlist" />
<input type="submit" value="使用色設定画面" />
</p>
</form>
END
	}
	print <<END;
<h2>掲示板の初期化</h2>
<p>掲示板を全て初期化して、使用できるようにします。</p>
<p>初期化した場合、全てのデータが消えるので注意して下さい。</p>
<form action="admin.cgi" method="post">
<p>
<input type="hidden" name="password" value="$ini::password" />
<input type="hidden" name="mode" value="init2" />
<input type="submit" name="sub" value="初期化" disabled />
<label>
<input type="checkbox" onclick="this.form.elements.item('sub').disabled=false" />
本当に初期化する
</label>
</p>
</form>
</body>
</html>
END
exit(0);
sub wrongpassword{
		print <<END;
<p><strong>エラー</strong>：パスワードが違います。</p>
</article>
</body>
</html>
END
}
sub loging{
		print <<END;
<article>
<h1>ログイン</h1>
<p>管理者ページにログインして下さい。</p>
<form action="admin.cgi" method="post">
<p>
<input type="hidden" name="mode" value="login" />
パスワード：<input type="password" name="password" size="30" /></p>
<p><input type="submit" value="ログイン" /></p>
</form>
</article>
</body>
</html>
END
}


sub administer{
	$Global_admin_mode=1;
	$top_mode="table";
	if($cgi->param('number')){
		my($number)=$cgi->param('number');
		data::view($number,-1,$cgi,"normal");
	}else{
		output::topheader();
		data::threads_table(-1);
		output::footer();
	}
}
sub change{
	my($perm)=sprintf("%3o",$ini::filePermission);
	print <<END;
<article class="form">
<h1>設定変更</h1>
<form action="admin.cgi" method="post">
<input type="hidden" name="password" value="$ini::password" />
<input type="hidden" name="mode" value="changeini" />
<p>
<b>掲示板の名前:</b>
<input type="text" size="40" name="bbsName" value="$ini::bbsName" />
</p>
<p>
<b>掲示板の説明:</b>
<input type="text" size="40" name="bbsDescription" value="$ini::bbsDescription" />
</p>
<p>
<b>パスワード:</b>
<input type="text" size="40" name="newPassword" value="$ini::password" /><br />
パスワードは他人に知られないようなものにして下さい。
</p>
<p>
<b>サイトのURL:</b>
<input type="text" size="40" name="site" value="$ini::site" /><br />
掲示板を設置しているサイトのURLを入力して下さい。
</p>
<p>
<b>データフォルダ名:</b>
$ini::data<br />
この設定は管理画面から変更できません。
</p>
<p>
<b>ロックフォルダ名:</b>
<input type="text" size="40" name="lockdir" value="$ini::lockdir" /><br />
ロックフォルダ名は、適当なフォルダ名を入力して下さい。フォルダは自動で作られるので、そのフォルダを作る必要はありません。
</p>
<p>
<b>ファイルパーミッション:</b>
<input type="text" size="40" name="filePermission" value="$perm" /><br />
データファイルのファイルパーミッションを指定します。
</p>
<p>
<b>名前が空の場合に使う名前:</b>
<input type="text" size="40" name="noName" value="$ini::noName" /><br />
空にすると、名前が空の場合エラーが出ます。
</p>
<p>
<b>1ページに表示するスレッドの数:</b>
<input type="text" size="20" name="page_threads" value="$ini::page_threads" />
</p>
<p>
<b>1ページに表示するレスの数:</b>
<input type="text" size="20" name="page_res" value="$ini::page_res" />
</p>
<p>
<b>検索時の最大表示件数:</b>
<input type="text" size="20" name="search_max" value="$ini::search_max" />
</p>
<p>
<b>パスワード無しを許可するか:</b>
<select name="noPassword">
END
	my($noPassword_ch1)=$ini::noPassword==0 ? " selected" : "";
	my($noPassword_ch2)=$ini::noPassword!=0 ? " selected" : "";
	my($delete_free_ch1)=$ini::delete_free==0 ? " selected" : "";
	my($delete_free_ch2)=$ini::delete_free!=0 ? " selected" : "";
	my($use_trip_ch1)=$ini::use_trip==0 ? " selected" : "";
	my($use_trip_ch2)=$ini::use_trip!=0 ? " selected" : "";
	my($use_akukin_ch1)=$ini::use_akukin==0 ? " selected" : "";
	my($use_akukin_ch2)=$ini::use_akukin==1 ? " selected" : "";
	my($use_akukin_ch3)=$ini::use_akukin==2 ? " selected" : "";
	my($use_URL_ch1)=$ini::use_URL==0 ? " selected" : "";
	my($use_URL_ch2)=$ini::use_URL!=0 ? " selected" : "";
	my($use_email_ch1)=$ini::use_email==0 ? " selected" : "";
	my($use_email_ch2)=$ini::use_email!=0 ? " selected" : "";
	my($use_color_ch1)=$ini::use_color==0 ? " selected" : "";
	my($use_color_ch2)=$ini::use_color==1 ? " selected" : "";
	my($use_color_ch3)=$ini::use_color==2 ? " selected" : "";
	print <<END;
<option value="0"$noPassword_ch1>許可しない</option>
<option value="1"$noPassword_ch2>許可する</option>
</select>
</p>
<p>
<b>投稿者が編集・削除機能を使えるか:</b>
<select name="delete_free">
<option value="0"$delete_free_ch1>使えない</option>
<option value="1"$delete_free_ch2>使える</option>
</select>
</p>
<p>
<b>トリップ機能を使用するか:</b>
<select name="use_trip">
<option value="0"$use_trip_ch1>使用しない</option>
<option value="1"$use_trip_ch2>使用する</option>
</select>
</p>
<p>
<b>アクセス禁止機能を使うか:</b>
<select name="use_akukin">
<option value="0"$use_akukin_ch1>使用しない</option>
<option value="1"$use_akukin_ch2>書き込み時</option>
<option value="2"$use_akukin_ch3>アクセス時</option>
</select><br />
</p>
<p>
<b>URLを入力・表示するか:</b>
<select name="use_url">
<option value="0"$use_URL_ch1>使用しない</option>
<option value="1"$use_URL_ch2>使用する</option>
</select>
</p>
<p>
<b>メールアドレスを入力・表示するか:</b>
<select name="use_email">
<option value="0"$use_email_ch1>使用しない</option>
<option value="1"$use_email_ch2>使用する</option>
</select>
</p>
<p>
<b>レスの色:</b>
<select name="use_color">
<option value="0"$use_color_ch1>選択しない</option>
<option value="1"$use_color_ch2>一覧から選択する</option>
<option value="2"$use_color_ch3>自由に選択する</option>
</select>
</p>
<p><b></b><input type="submit" value="送信" /></p>
</form>
</article>
</body>
</html>
END
}
sub changeini{
	unless(data::filelock()){
		output::error2("設定変更に失敗しました。");
		change();
		return;
	}
	my($bbsName)=$cgi->param('bbsName');
	my($bbsDescription)=$cgi->param('bbsDescription');
	my($newPassword)=$cgi->param('newPassword');
	my($site)=$cgi->param('site');
	my($lockdir)=$cgi->param('lockdir');
	my($filePermission)=$cgi->param('filePermission');
	my($noName)=$cgi->param('noName');
	my($noPassword)=int($cgi->param('noPassword'));
	my($page_threads)=int($cgi->param('page_threads'));
	my($page_res)=int($cgi->param('page_res'));
	my($search_max)=int($cgi->param('search_max'));
	my($delete_free)=int($cgi->param('delete_free'));
	my($use_trip)=int($cgi->param('use_trip'));
	my($use_akukin)=int($cgi->param('use_akukin'));
	my($use_URL)=int($cgi->param('use_url'));
	my($use_email)=int($cgi->param('use_email'));
	my($use_color)=int($cgi->param('use_color'));

	unless(writeini($bbsName,$bbsDescription,$newPassword,$site,$ini::data,
	$lockdir,$filePermission,$noName,$noPassword,
	$page_threads,$page_res,$search_max,$delete_free,
	$use_trip,$use_akukin,$use_URL,$use_email,$use_color)){
		output::error2("設定変更に失敗しました。");
		data::fileunlock();
		change();
		return;
	}
	data::fileunlock();
	print <<END;
<p>設定を変更しました。</p>
<p><a href="index.cgi">掲示板に入る</a>｜<a href="admin.cgi?mode=login&password=$ini::password">管理者ページに戻る</a></p>
</article>
</body>
</html>
END
}
sub init_ini{
	return writeini($ini::bbsName,$ini::bbsDescription,$cgi->param('newpassword'),
	$ini::site,$cgi->param('data'),$ini::lockdir,sprintf("%03o",$ini::filePermission),
	$ini::noName,$ini::noPassword,$ini::page_threads,$ini::page_res,
	$ini::search_max,$ini::delete_free,$ini::use_trip,$ini::use_akukin,$ini::use_URL,$ini::use_email,$ini::use_color);
	
}
# ini書き換え　成功:1 失敗:0
sub writeini{
	my($bbsName,$bbsDescription,$newPassword,$site,$data,$lockdir,$filePermission,
	$noName,$noPassword,$page_threads,$page_res,$search_max,$delete_free,
	$use_trip,$use_akukin,$use_URL,$use_email,$use_color) = @_;

	$bbsName =~ s/\"/\\\"/g;
	$bbsDescription =~ s/\"/\\\"/g;
	$newPassword =~ s/\"/\\\"/g;
	$site =~ s/\"/\\\"/g;
	$lockdir =~ s/\"/\\\"/g;
	$noName =~ s/\"/\\\"/g;

	$filePermission =~ s/[^0-7]/6/g;
	while(length($filePermission)<3){
		$filePermission="0".$filePermissiomn;
	}
	if($filePermission=~/(...).+/){
		$filePermission=$1;
	}
	unless(open(FILE,">ini.cgi")){
		return 0;
	}
	print FILE <<END;
package ini;
#ini:設定

#タイムゾーン
\$timezone = "$ini::timezone";

#掲示板の名前
\$bbsName = "$bbsName";

#掲示板の説明
\$bbsDescription = "$bbsDescription";

#パスワード
\$password = "$newPassword";

#サイト
\$site = "$site";

#データフォルダ名
\$data = "$data";

#ロックフォルダ名
\$lockdir = "$lockdir";

#ファイルのパーミッション
\$filePermission = 0$filePermission;

#名無しの名前（""なら名無しを許可しない）
\$noName = "$noName";

#パスワード無しを許可するか（1なら許可、0なら許可しない）
\$noPassword = $noPassword;

# 1ページのスレッドの数
\$page_threads=$page_threads;

# 1ページのレスの数
\$page_res=$page_res;

# 検索時の最大表示件数
\$search_max=$search_max;

# 誰でも自分の投稿を削除できるか
\$delete_free=$delete_free;

# トリップ機能を使用するか
\$use_trip=$use_trip;

# アクセス禁止機能を使用するか
\$use_akukin=$use_akukin;

# URLを使用するか
\$use_URL=$use_URL;

# メールアドレスを使用するか
\$use_email=$use_email;

# 色を使用するか (0:使用しない 1:一覧から選択 2:自由選択）
\$use_color=$use_color;

return 1;
END
	close(FILE);
	return 1;
}
sub akukin{
	my($file)="";
	if(open(FILE,"$ini::data/akukin.cgi")){
		while(<FILE>){
			$file.=$_;
		}
		close(FILE);
	}
	print <<END;
<p><a href="admin.cgi?mode=login&password=$ini::password">管理者ページに戻る</a></p>
<article class="form">
<h1>アクセス禁止設定画面</h1>
<form action="admin.cgi" method="post">
<p>
<input type="hidden" name="password" value="$ini::password" />
<input type="hidden" name="mode" value="changeakukin" />
1行に1つIPアドレスを記入することで、そのIPアドレスからの書き込みを禁止することができます。</p>
<p>また、スラッシュを使った記法（例：192.168.1.0/24は192.168.1.0～192.168.1.255までの範囲を表す）を使用することができます。</p>
<p><textarea name="akukins" cols="30" rows="8">
$file</textarea></p>
<p><input type="submit" value="送信" /></p>
</form>
</article>
</body>
</html>
END
}
sub changeakukin{
	my(@lines)=split(/\r\n|\n|\r/,$cgi->param('akukins'));
	open(FILE,">$ini::data/akukin.cgi");
	foreach(@lines){
		chomp;
		print FILE "$_\n";
	}
	close(FILE);
	print <<END;
<p>設定を変更しました。</p>
<p><a href="index.cgi">掲示板に入る</a>｜<a href="admin.cgi?mode=login&password=$ini::password">管理者ページに戻る</a></p>
</article>
</body>
</html>
END
}
sub style{
	unless(opendir(DH,"css")){
		output::error2("cssのディレクトリを開けませんでした。");
		output::footer();
		return;
	}
	my(@files,$f);
	@files = grep{$_!~/^\.+$/; }readdir DH;
	closedir(DH);
	print <<END;
<article class="form">
<h1>スタイル設定画面</h1>
<form action="admin.cgi" method="post">
<p>
<input type="hidden" name="password" value="$ini::password" />
<input type="hidden" name="mode" value="changestyle" />
セレクトボックスから、使用するスタイルシートのファイルを選択して下さい。</p>
<p>
<select name="css">
END
	foreach(@files){
		print <<END;
<option value="$_">$_</option>
END
	}
	print <<END;
</select></p>
<p><input type="submit" value="送信" /></p>
</form>
</article>
</body>
</html>
END
}
sub changestyle{
	my($file)=$cgi->param('css');
	unless(-e "css/$file"){
		output::error2("ファイルがありません。");
		output::footer();
		return;
	}
	open(FILE, "css/$file");
	open(FO, ">style.css");
	while(<FILE>){
		print FO;
	}
	close(FO);
	close(FILE);
	print <<END;
<p>設定を変更しました。</p>
<p>すぐに変更が反映されない場合があります。その場合は、管理画面に戻ってからブラウザを「更新」しましょう。</p>
<p><a href="index.cgi">掲示板に入る</a>｜<a href="admin.cgi?mode=login&password=$ini::password">管理者ページに戻る</a></p>
</article>
</body>
</html>
END
}
sub kinsi{
	my($file)="";
	if(open(FILE,"$ini::data/kinsi.cgi")){
		while(<FILE>){
			$file.=$_;
		}
		close(FILE);
	}
	print <<END;
<p><a href="admin.cgi?mode=login&password=$ini::password">管理者ページに戻る</a></p>
<article class="form">
<h1>禁止ワード設定画面</h1>
<form action="admin.cgi" method="post">
<p>
<input type="hidden" name="password" value="$ini::password" />
<input type="hidden" name="mode" value="changekinsi" />
1行に1つ禁止ワードを記入することで、それを含む投稿ができなくなります。</p>
<p><textarea name="kinsis" cols="30" rows="8">
$file</textarea></p>
<p><input type="submit" value="送信" /></p>
</form>
</article>
</body>
</html>
END
}
sub changekinsi{
	my(@lines)=split(/\r\n|\n|\r/,$cgi->param('kinsis'));
	open(FILE,">$ini::data/kinsi.cgi");
	foreach(@lines){
		chomp;
		print FILE "$_\n";
	}
	close(FILE);
	print <<END;
<p>設定を変更しました。</p>
<p><a href="index.cgi">掲示板に入る</a>｜<a href="admin.cgi?mode=login&password=$ini::password">管理者ページに戻る</a></p>
</article>
</body>
</html>
END
}
sub colorlist{
	my(@c_name)=();
	my(@c_value)=();
	my($l_number)=0;
	if(open(FILE,"$ini::data/colorlist.cgi")){
		while(<FILE>){
			chomp;
			($c_name[$l_number],$c_value[$l_number])=split(/\t/);
			$l_number++;
		}
		close(FILE);
	}
	print <<END;
<p><a href="admin.cgi?mode=login&password=$ini::password">管理者ページに戻る</a></p>
<article class="form">
<h1>使用色設定画面</h1>
<p>※JavaScriptを使用します。</p>
<form action="admin.cgi" method="post" onsubmit="subm(event)">
<input type="hidden" name="password" value="$ini::password" />
<input type="hidden" name="mode" value="changecolorlist" />
<input type="hidden" name="listnumber" value="$l_number" />
<table id="colorlisttable">
<caption>色一覧</caption>
<tr><th>色名</th><th>色</th></tr>
END
	my($cnt)=0;
	foreach(@c_name){
		$_=~ s/'//g;
		print "<tr><td><input type='text' size='20' name='cname' value='$_' /></td>";
		print "<td><input type='color' value='".$c_value[$cnt]."' name='cvalue' />";
		print "<input type='button' name='deleteButton' value='削除' /></td>\n";

		$cnt++;
	}
	print <<END;
</table>
<p><input type="button" name="addButton" value="色追加" /></p>
<p><input type="submit" value="送信" /></p>
</form>
</article>
<script type="text/javascript">
if(document.addEventListener){
	document.addEventListener("click",clicked,false);
}else if(document.attachEvent){
	document.attachEvent("onclick",clicked);
}

function clicked(e){
	var t=e.target||e.srcElement;

	if(t.name=="deleteButton"){
		var tr=findParentT(t,"tr");
		var table=findParentT(tr,"table");

		table.deleteRow(tr.rowIndex);
	}else if(t.name=="addButton"){
		var table=document.getElementById("colorlisttable");

		var tr=table.insertRow(-1);

		var td1=tr.insertCell(0);
		var input=document.createElement("input");
		input.type="text";input.size=20;
		input.name="cname";
		input.value="";
		td1.appendChild(input);

		var td2=tr.insertCell(1);
		input=document.createElement("input");
		input.type="color";
		input.name="cvalue";
		input.value="#000000";
		td2.appendChild(input);

		input=document.createElement("input");
		input.type="button";
		input.name="deleteButton";
		input.value="削除";
		td2.appendChild(input);
	}


}
function subm(e){

	var names=document.getElementsByName("cname");
	var query=[];
	for(var i=0,l=names.length;i<l;i++){
		query[query.length]=names[i];
	}
	for(var i=0,l=query.length;i<l;i++){
		var tr=findParentT(query[i],"tr");
		query[i].name="cname"+(tr.rowIndex-1);
	}

	names=document.getElementsByName("cvalue");
	query=[];
	for(var i=0,l=names.length;i<l;i++){
		query[query.length]=names[i];
	}
	for(var i=0,l=query.length;i<l;i++){
		var tr=findParentT(query[i],"tr");
		query[i].name="cvalue"+(tr.rowIndex-1);
	}
	document.getElementsByName("listnumber")[0].value=l;
}
function findParent(node,judge){
	do{
		if(judge(node))return node;
	}while(node=node.parentNode);
}
function findParentT(node,tag){
	tag=tag.toLowerCase();
	return findParent(node,function(obj){return obj.tagName.toLowerCase()==tag});
}
</script>
</body>
</html>
END
}
sub changecolorlist{
	open(FILE,">$ini::data/colorlist.cgi");
	my($l)=int($cgi->param('listnumber'));
	for(my $i=0;$i<$l;$i++){
		my($cname)=$cgi->param("cname$i");
		my($cvalue)=$cgi->param("cvalue$i");
		$cname=~ s/\t/ /g;
		if($cvalue !~ /^\s*(#[0-9a-fA-F]{6})\s*$/){
			next;
		}
		print FILE $cname."\t".$cvalue."\n";
	}
	close(FILE);
	print <<END;
<p>設定を変更しました。</p>
<p><a href="index.cgi">掲示板に入る</a>｜<a href="admin.cgi?mode=login&password=$ini::password">管理者ページに戻る</a></p>
</article>
</body>
</html>
END
}

