function check_input(e){
	var t = e.target || e.srcElement;
	if(!t)return;
	if(noPassword==0 && t.elements["password"].value==""){
		ev_err(e,"パスワードが入力しての");
		return false;
	}
	if(noName=="" && t.elements["name"].value==""){
		ev_err(e,"名前がないよ");
		return false;
	}
	if(t.elements["title"].value==""){
		ev_err(e,"なんか変ばい。スレタイか本文が空や");
		return false;
	}
	if(t.elements["message"].value==""){
		ev_err(e,"本文が空ですばい！");
		return false;
	}
}
function ev_err(e,mes){
	if(e.preventDefault){
		e.preventDefault();
	}else{
		e.returnValue=false;
	}
	var err=document.getElementById('error_message');
	if(err){
		err.innerHTML=mes;
	}
}
/*@cc_on
@if ( @_jscript_version <= 5.8)
var ie_elements=[
	'section', 'article', 'hgroup', 'header',
	'footer', 'nav', 'aside', 'figure',
	'figcaption', 'mark', 'time', 'meter', 'progress'
];
for(var i=0,l=ie_elements.length;i<l;i++){
	document.createElement(ie_elements[i]);

}@end @*/

