// $(document).ready(function(){
var ip_amount = function(e){
    return e.tdValue('ipKey').split('.').reduce(function(a,b){return parseInt(a)+parseInt(b)});
};
// ip comparison
var ip_asc = function(a,b){
    return ip_amount(a)-ip_amount(b)
};
var ip_desc = function(a,b){
    return ip_amount(b)-ip_amount(a)
};
// date comparison
var date_asc = function(a,b){
    var d1 = Date.parse(a.tdValue('registKey'));
    var d2 = Date.parse(b.tdValue('registKey'));
    // empty date  greater than any date
    if(isNaN(d1)&&isNaN(d2)){
        return  ip_asc(a,b);
    }else if(isNaN(d1)){
        return  1;
    }else if(isNaN(d2)){
        return -1;
    };
    var r = d1-d2;
    if(r==0){
        return ip_asc(a,b);
    }else{
        return r;
    };
};
var date_desc = function(a,b){
    var d1 = Date.parse(a.tdValue('registKey'));
    var d2 = Date.parse(b.tdValue('registKey'));
    // empty date  greater than any date
    if(isNaN(d1)&&isNaN(d2)){
        return  ip_asc(a,b);
    }else if(isNaN(d1)){
        return  1;
    }else if(isNaN(d2)){
        return -1;
    };
    var r = d2-d1;
    if(r==0){
        return ip_asc(a,b);
    }else{
        return r;
    };
};
// alive comparsion
function alive_asc(a,b){
    var r = parseInt(a.tdClass('aliveKey')) - parseInt(b.tdClass('aliveKey'));
    if(r==0){
        return date_desc(a,b)
    }else{
        return r;
    };

};
function alive_desc(a,b){
    var r = parseInt(b.tdClass('aliveKey')) - parseInt(a.tdClass('aliveKey'));
    if(r==0){
        return date_asc(a,b)
    }else{
        return r;
    };
};
function sortColumn(index,ascCmp,descCmp){
    // desc first then asc 
    var toggle = 0;// 0:desc 1:asc
    $('#detail thead th').eq(index).click(function(){
        var cmp = toggle ? ascCmp :descCmp;
        trs.sort(cmp);
        reset();
        toggle ? this.className='order-asc' : this.className='order-desc';
        toggle = toggle^1;//reversal
    });
};
Element.prototype.tdValue = function(k){return this.querySelectorAll('td')[thead[k]].innerText};
Element.prototype.tdClass = function(k){return this.querySelectorAll('td')[thead[k]].className};
function reset(){
    var tbody = $('#detail tbody');
    tbody.html('');
    var docfrag = document.createDocumentFragment();
    for(var i in trs){
        docfrag.appendChild(trs[i]);
    };
    tbody.append(docfrag);
};
//
var thead = {};
var trs = [];
$('#detail thead th').each(function(e){
    thead[this.id]=e;
});
$('#detail tbody tr').each(function(){
    trs.push(this);
});
// sort by ip
sortColumn(thead['ipKey'],ip_asc,ip_desc);
// sort by time
sortColumn(thead['registKey'],date_asc,date_desc);
// sort by lastdate
sortColumn(thead['aliveKey'],alive_asc,alive_desc);
// });
