var aui = (function(aui){

    aui.td = function(text){
        var td = document.createElement("td");
        td.appendChild(document.createTextNode(text));
        return td;
    };

    aui.tr = function(values){
        var tr = document.createElement("tr");
        for(key in values){
            tr.appendChild(aui.td(values[key]));
        }
        return tr;
    };

    aui.onElement = function(id,applyFunction){
        var element = document.getElementById(id);
        applyFunction(element);
    };

    return aui;
})(aui || {});