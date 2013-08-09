
// change style
function ChangeStyle(){
    var doc=document;
    var style=doc.createElement("style");
    style.setAttribute("type", "text/css");
    cssString = ".wrap{width:100% !important;margin:0 !important;}" +
                ".left{width:13% !important;}"+
                ".left, .header{margin-left: 0;}" +
                ".right{width:87% ;}.right .entry{margin: 0 5% 50px 0;}";

    if(style.styleSheet){ // IE
        style.styleSheet.cssText = cssString;
    } else {
        var cssText = doc.createTextNode(cssString);
        style.appendChild(cssText);
    }

    var heads = doc.getElementsByTagName("head");
    if(heads.length)
        heads[0].appendChild(style);
    else
        doc.documentElement.appendChild(style);
}

//search
function Search(){
    $("#search").toggle(666);
}