package ini;
#ini:設定

#タイムゾーン
$timezone = "+09:00";

#掲示板の名前
$bbsName = "掲示板";

#掲示板の説明
$bbsDescription = "";

#パスワード
$password = "password";

#サイト
$site = "";

#データフォルダ名
$data = "data";

#ロックフォルダ名
$lockdir = "lock";

#ファイルのパーミッション
$filePermission = 0666;

#名無しの名前（""なら名無しを許可しない）
$noName = "";

#パスワード無しを許可するか（1なら許可、0なら許可しない）
$noPassword = 1;

# 1ページのスレッドの数
$page_threads=10;

# 1ページのレスの数
$page_res=5;

# 検索時の最大表示件数
$search_max=50;

# 誰でも自分の投稿を削除できるか
$delete_free=1;

# トリップ機能を使用するか
$use_trip=0;

# アクセス禁止機能を使用するか
$use_akukin=0;

# URLを使用するか
$use_URL=1;

# メールアドレスを使用するか
$use_email=1;

# 色を使用するか (0:使用しない 1:一覧から選択 2:自由選択）
$use_color=1;

return 1;
