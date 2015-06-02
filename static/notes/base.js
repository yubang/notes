var page =1;
var lock =false;
function getNotes(){
    if(lock)return;
    lock=true;
    $.ajax({
        "url":"getNotes",
        "type":"get",
        "data":{"page":page},
        success:function(data){
            $(".content").append(data);
            lock=false;
        },
        error:function(e1,e2,e3){lock=false;},
    });    
    
}
