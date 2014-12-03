$(document).ready(function(){
// to the animate 
$('#totop').click(function(){
    $("html, body").animate({scrollTop: 0}, 230);
});
// tools
var host = $("input[name='host']");
var msg = $('#response');
$('#getmac').click(function(){
    msg.text("");
    $.get("/get",{host:host.val()})
        .done(function(r){
            msg.text(r)
        })
        .fail(function(r){
            msg.text("fail!")
        })
});
// table sort
var ip_asc = function(a,b){
    var ipa = $(a).find("td").eq(0).text().split('.').reduce(function(a,b){return parseInt(a)+parseInt(b)});
    var ipb = $(b).find("td").eq(0).text().split('.').reduce(function(a,b){return parseInt(a)+parseInt(b)});
    return ipa-ipb
};
var ip_desc = function(a,b){
    var ipa = $(a).find("td").eq(0).text().split('.').reduce(function(a,b){return parseInt(a)+parseInt(b)});
    var ipb = $(b).find("td").eq(0).text().split('.').reduce(function(a,b){return parseInt(a)+parseInt(b)});
    return ipb-ipa
};
function dateCmp(index,toggle){
    var date_asc = function(a,b){
        var d1 = Date.parse($(a).find("td").eq(index).text()).valueOf();
        var d2 = Date.parse($(b).find("td").eq(index).text()).valueOf();
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
        var d1 = Date.parse($(a).find("td").eq(index).text()).valueOf();
        var d2 = Date.parse($(b).find("td").eq(index).text()).valueOf();
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
    var cmp = toggle?date_asc:date_desc;
    return cmp;
};
var reset = function(){
    var tbody = $('tbody');
    tbody.html('');
    for(var i in trs){
      tbody.append(trs[i]);
    }
};
$('thead tr th:last').click(function(){
    // if(toggle==0){console.log('date_desc')}else if(toggle==1){console.log('date_asc')}else{console.log(toggle)};
    var index = $(this).index();
    var cmp = dateCmp(index,toggle);
    trs.sort(cmp);
    reset();
    toggle? $(this).attr("class","").addClass("order-asc"):$(this).attr("class","").addClass("order-desc");
    toggle = toggle^1;//reversal
});
$('thead tr th:first').click(function(){
    if(this.className=='order-asc'){
        var cmp = ip_desc;
        this.className='order-desc';
    }else{
        var cmp = ip_asc;
        this.className='order-asc';
    };
    trs.sort(cmp);
    reset();
});
var trs = [];
var toggle = 0;// 0:date_desc 1:date_asc
$('tbody tr').each(function(){
    trs.push(this);
});
});
