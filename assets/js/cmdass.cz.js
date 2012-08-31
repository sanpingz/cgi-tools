/**
 * Created with PyCharm.
 * User: sanpingz
 * Date: 12-8-15
 * Time: 下午1:31
 */
cz_command = {
    init : function(){
        $.getJSON('command.json',function(data){
            var str = '';
            $(data.command).each(function(i, e){
                str += '<option value="'+e.value+'">'+e.label+'</option>';
            })
            $("#command-select").append(str)
        });
    },
    change : function(){
        $("#command-select").change(function(){
            var value = $(this).val();
            $.getJSON('command.json',function(data){
                if(data.parameter.hasOwnProperty(value) && data.parameter[value].length>0){
                    var param = data.parameter[value];
                    var e = param[0].input.name;
                    alert(e);
                }
            });
        });
    }
}