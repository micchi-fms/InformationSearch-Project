$(function(){
    for(let i=1947; i < 2012; i++){
        $('#container').append('<li >'+i+'</li>');
    }    

    //クリック
    $('#container li').click(function(){
        var text = $(this).text();
        $("#tokuchou_container").empty();
        $('#dialog').empty();
        $('#dialog_number').empty();
        console.log('テキスト:' + text);
        GetTokuchou(text);
    });

    function GetTokuchou(_year){
        $.get('http://127.0.0.1:5000/year?year='+_year)
        .done( function(data) {
            console.log(data);
            console.log(data['tokuchou']);
            ListTokuchou(data['tokuchou'],_year);
        } )
        .fail( function(err) {
            console.log('ERROR:'+err);    
        })
    }

    function ListTokuchou(_data,_year){
        for(let v of _data){
            $('#tokuchou_container').append('<li >'+v+'</li>');
        }

        //クリック
        $('#tokuchou_container li').click(function(){
            var text = $(this).text();
            console.log('ListTokuchou _year:'+_year);
            $('#dialog').empty();
            $('#dialog_number').empty();
            GetDialogue(_year,text);
        });
    }

    function GetDialogue(_year,_word){
        $.get('http://127.0.0.1:5000/yearWord/'+_year+'?word='+_word)
        .done( function(data) {
            console.log(data);
            ListDialogue(data);
        } )
        .fail( function(err) {
            console.log('ERROR:'+err);    
        })
    }

    function ListDialogue(_data){
        var list=_data['result']
        // $('#dialog').before('<p>'+list.length+'</p>')
        $('#dialog_number').text('総文章数'+list.length);
        $('#dialog').append('<tr><th>日付</th><th>発言者</th><th>内容</th></tr>');
        for(var l of list){
            var date =new Date(l[1]);
            var sdate =date.getFullYear() + "/" +  date.getMonth() + 1 + "/"+ date.getDate()  + "/" + date.getDay();
            $('#dialog').append('<tr><td>'+sdate+'</td><td>'+l[2]+'</td><td>'+l[5]+'</td></tr>');
        }
    }

});