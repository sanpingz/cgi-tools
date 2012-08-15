/**
 * Created with PyCharm.
 * User: sanpingz
 * Date: 12-8-9
 * Time: 下午1:57
 * To change this template use File | Settings | File Templates.
 */
start_call={
    init : function(){
        $("#start_form").submit(function(){
            if($("#input01").val()==''&&$("#input02").val()==''){
                $("#labip").addClass("warning");
                $("#callid").addClass("warning");
            }else if($("#input01").val()==''&&$("#input02").val()!=''){
                $("#labip").addClass("warning");
            }else if($("#input01").val()!=''&&$("#input02").val()==''){
                $("#callid").addClass("warning");
            }else{
                $("#ajax_load").show();
                var data = $("#start_form").serialize();
                var uri = 'start.cgi';
                $.post(uri, data, function(data){
                    $("tbody").append(data);
                });
                $("#call_back").fadeIn(4000);
                $("#ajax_load").delay(3000).fadeOut();
            };
            return false;
        });
        $('#stop_form button[type=button]').live('click',function(){
            $("#ajax_load").show();
            var uri = 'stop.cgi';
            var parent = $(this).parent('td');
            var ctid = parent.find('input[name=ctid]').val();
            var labip = parent.find('input[name=labip]').val();
            var status = parent.parent('tr').find('.cb_status').first();
            status.empty();
            status.append('<div> Checking </div>');
            var button = $(this);
            button.attr("disabled", true);
            $.post(uri, {ctid: ctid, labip: labip}, function(data){
                button.delay(10000).slideUp(100,function(){
                    status.empty();
                    status.append('<div> '+data+' </div>');
                    status.empty();
                    status.append('<div> Checking </div>');
                    var a = button.next('a');
                    uri = 'download.cgi';
                    $.post(uri, {ctid: ctid, labip: labip}, function(data){
                        status.empty();
                        if(data.length>1){
                            a.slideDown(100);
                            a.attr('href', data);
                            status.append('<div> OK </div>');
                        }else{
                            status.append('<div> Failure </div>');
                            button.slideDown();
                        }
                    });
                });
            });
            $("#ajax_load").delay(10000).fadeOut();
            return false;
        });
    },
    rmClass:function(){
        $("#input01").blur(function(){
            if($(this).val()==''){
                $("#labip").addClass("warning");
            }else{
                $("#labip").removeClass("warning");
            }
        });
        $("#input02").blur(function(){
            if($(this).val()==''){
                $("#callid").addClass("warning");
            }else{
                $("#callid").removeClass("warning");
            }
        });
    }
}