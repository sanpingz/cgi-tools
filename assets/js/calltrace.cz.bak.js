/**
 * Created with PyCharm.
 * User: sanpingz
 * Date: 12-8-9
 * Time: 下午1:57
 * To change this template use File | Settings | File Templates.
 */
start_call={
    start : function(){
        var ip = $("#labip"),
            trace = $("#callid"),
            dur = $("#duration");
        function updateTips(d, t) {
            d.addClass( "warning" );
            d.find("p").first().text( t );
        }
        function checkInt(d, t, max){
            var s = d.find('input').first();
            if(s.val()=='' || s.val()!=parseInt(s.val(),10) || parseInt(s.val(),10)<=0||parseInt(s.val(),10)>max){
                updateTips(d ,t);
                return false;
            }else{
                updateTips(d ,'OK');
                d.removeClass('warning');
                return true;
            }
        }
        function checkRegexp(p, d, t){
            if(!p.test(d.find('input').first().val())){
                updateTips(d ,t);
                return false
            }else{
                updateTips(d ,'OK');
                d.removeClass('warning');
                return true;
            }
        }
        function checkIP(){
            var reg = /^(?:(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))$/;
            return checkRegexp(reg, ip, 'Please input a valid IP.');
        }
        function checkCallId(){
            var mode = $("#select01").val();
            var valid = false;
            var reg = /\w+/;
            if(mode == 'SIPURI'){
                reg = /sip(s?)\:[\w\.\-\+]+@([\w\-]+\.)+[a-zA-Z]/;
                valid = checkRegexp(reg ,trace, 'Please input a valid sip uri.');
                valid = valid && ($("#input02").val().length<=63);
            }else if(mode == 'TELNUM'){
                reg = /^\d{4,32}$/;
                valid = checkRegexp(reg ,trace, 'Please input a valid telephone number.');
            }else if(mode == 'MGWID'){
                reg = /^\w{4,256}$/;
                valid = checkRegexp(reg ,trace, 'Please input a valid gateway id.');
            }
            return valid;
        }
        function checkDuration(){
            return checkInt(dur, 'Please input a valid duration.', 60);
        }
        document.getElementById("input01").onblur = function(){
            checkIP();
        }
        document.getElementById("input02").onblur = function(){
            checkCallId();
        }
        document.getElementById("input03").onblur = function(){
            checkDuration();
        }
        $("#select01").change(function(){
            if(!checkCallId()){
                $("#input02").val('');
            }
        });
        $("#start_form").submit(function(){
            var valid = true;
            valid = valid && checkIP();
            valid = valid && checkCallId();
            valid = valid && checkDuration();
            if(valid){
                $("#ajax_load").show();
                var data = $("#start_form").serialize();
                var uri = 'start.cgi';
                var handle = $("#username").text();
                data += '&handle='+handle;
                $.post(uri, data, function(data){
                    $("tbody").append(data);
                });
                $("#call_back").fadeIn(4000);
                $("#ajax_load").delay(3000).fadeOut();
            };
            return false;
        });
    },
    stop : function(){
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
            var handle = $("#username").text();
            $.post(uri, {ctid: ctid, labip: labip, handle:handle}, function(data){
                button.delay(8000).fadeTo(100,0.8,function(){
                    status.empty();
                    status.append('<div> '+data+' </div>');
                    status.empty();
                    status.append('<div> Checking </div>');
                    var a = button.next('a');
                    uri = 'download.cgi';
                    $.post(uri, {ctid: ctid, labip: labip, handle: handle}, function(data){
                        status.empty();
                        if(data.length>1){
                            button.hide();
                            a.slideDown(100);
                            a.attr('href', data);
                            status.append('<div> Stopped </div>');
                        }else{
                            status.append('<div> Failure </div>');
                        }
                    });
                });
            });
            $("#ajax_load").delay(8000).fadeOut();
            return false;
        });
    },
    load : function(){
        var handle = $("#username").text();
        if(handle!='handle'){
            $.post('load.cgi', { handle:handle}, function(data){
                if(data.length>1){
                    $("tbody").append(data);
                    $("#call_back").fadeIn(4000);
                }
            });
        }
    },
    check : function(){
        $(function() {
            var cookie = cz_cookie.createCookie();
            $( "#dialog:ui-dialog" ).dialog( "destroy" );
            var handle = $( "#handle" ),
                allFields = $( [] ).add( handle ),
                tips = $( ".validateTips" );
            function updateTips( t ) {
                tips
                    .text( t )
                    .addClass( "ui-state-highlight" );
                setTimeout(function() {
                    tips.removeClass( "ui-state-highlight", 1500 );
                }, 500 );
            }
            function checkLength( o, n) {
                if (o.val()==null && o.val()=='' ) {
                    o.addClass( "ui-state-error" );
                    updateTips( n+ "is requires." );
                    return false;
                } else {
                    return true;
                }
            }
            function checkRegexp( o, regexp, n ) {
                if ( !( regexp.test( o.val() ) ) ) {
                    o.addClass( "ui-state-error" );
                    updateTips( n );
                    return false;
                } else {
                    return true;
                }
            }
            function checkHandle(o, n){
                updateTips( "Checking ... " );
                $.post('check.cgi',{ handle: o.val() },function(data){
                    if(data.length>1){
                        var value = handle.val();
                        $("#username").replaceWith('<span id="username">'+value+'</span>');
                        if($("#remember").attr('checked')){
                            cookie.set('handle',value,365);
                        }else{
                            cookie.del('handle');
                        }
                        $("#dialog-form").dialog( "close" );
                        $("#main-tab").show();
                        start_call.load()
                    }else{
                        updateTips( n );
                    }
                })
            }
            $( "#dialog-form" ).dialog({
                autoOpen: false,
                height: 290,
                width: 420,
                modal: true,
                closeOnEscape: false,
                buttons: {
                    "Confirm": function() {
                        var bValid = true;
                        allFields.removeClass( "ui-state-error" );
                        bValid = bValid && checkLength( handle, "Handle" );
                        bValid = bValid && checkRegexp( handle, /^[a-z]([0-9a-z_])+$/i, "Handle may consist of a-z, 0-9, underscores, begin with a letter." );
                        if ( bValid ) {
                            /*code*/
                            checkHandle( handle, "Oops, we don't find your handle, please try again!" );
                        }
                    },
                    Cancel: function() {
                        $( this).dialog({ disabled: true });
                    }
                },
                close: function() {
                    allFields.val( "" ).removeClass( "ui-state-error" );
                }
            });
            if(cookie.check('handle')){
                /*code*/
                $("#username").replaceWith('<span id="username">'+cookie.get('handle')+'</span>');
                $("#main-tab").show();
                start_call.load()
            }else{
                $("#dialog-form").dialog( "open" );
                $("#handle").focus();
                $(this).bind("keypress.ui-dialog", function(event) {
                    if (event.keyCode == $.ui.keyCode.ENTER) {
                        $(".ui-dialog-buttonpane button").first().click();
                        return false;
                    }
                });
            }
        });
    },
    feedback : function(){
        $(function() {
            $( "#dialog:ui-dialog" ).dialog( "destroy" );
            var content = $( "#mail-content" ),
                handle = $( "#username" ),
                allFields = $( [] ).add(content),
                tips = $( "#mail-tips" );
            function updateTips( t ) {
                tips
                    .text( t )
                    .addClass( "ui-state-highlight" );
                setTimeout(function() {
                    tips.removeClass( "ui-state-highlight", 1500 );
                }, 500 );
            }
            function checkLength( o, m, len) {
                String.prototype.trim = function() {
                    return this.replace(/(^\s*)|(\s*$)|(\n)/gm, '');
                }
                var value = o.val().trim();
                if (value=='' || value.length<len ) {
                    o.addClass( "ui-state-error" );
                    updateTips( m );
                    return false;
                } else {
                    return true;
                }
            }
            function checkHandle() {
                if ( $("#username").text() == "handle" ) {
                    updateTips( "Please authenticate first!" );
                    return false;
                } else {
                    return true;
                }
            }
            function SendMail() {
                var data = $("#send-form").serialize();
                data += "&handle="+handle.text();
                updateTips( "Sending" );
                $.post('mail.cgi', data, function(data){
                    if(data.length>1){
                        updateTips( "Oops, we have tried our best, please try again!" );
                    }else{
                        updateTips( "Your comments were sent successfully, thank you." );
                    }
                });
            }
            $( "#mail-form" ).dialog({
                autoOpen: false,
                height: 360,
                width: 560,
                modal: true,
                buttons: {
                    "Confirm": function() {
                        var bValid = true;
                        allFields.removeClass( "ui-state-error" );
                        bValid = bValid && checkHandle();
                        bValid = bValid && checkLength( content, "Detail information could help us.",10 );
                        if ( bValid ) {
                            /*code*/
                            SendMail();
                        }
                    },
                    Cancel: function() {
                        $( this).dialog( "close" );
                    }
                },
                close: function() {
                    allFields.val( "" ).removeClass( "ui-state-error" );
                    updateTips( "Any questions and suggestions are welcomed!" );
                }
            });
            $("#feedback").click(function(){
                $("#mail-form").dialog( "open" );
                $("#subject").focus();
            });
        });
    }
}

cz_cookie = {
    createCookie : function(){
        var cookie = new Object();
        cookie.set = function(name, value, duration){
            if(name!=null && name!='' && value!=null && value!=''){
                var exp = new Date();
                exp.setDate(exp.getDate()+duration);
                document.cookie = name+'='+value+((duration==null)? "":";expires="+exp.toGMTString());
            }
        }
        cookie.get = function(name){
            if(document.cookie.length>0){
                var start = document.cookie.indexOf(name+'=');
                var value = '';
                if(start != -1){
                    start += name.length+1;
                    var end = document.cookie.indexOf(';', start);
                    if(end == -1){
                        end = document.cookie.length;
                    }
                    value = document.cookie.substring(start, end);
                }
            }
            return value;
        }
        cookie.del = function(name){
            var exp = new Date();
            exp.setTime(exp.getTime() - 1);
            var duration= this.get(name);
            if(duration!=null) document.cookie= name + "="+duration+";expires="+exp.toGMTString();
        }
        cookie.check = function(name){
            var value = this.get(name);
            if(value != null && value != ''){
                return true;
            }
            return false;
        }
        return cookie;
    }
}

cz_event = {
    init: function(){
        $("#select01").click(function () {
            var type = $(this).val();
            if (type == 'TELNUM') {
                $("#macthdir").show();
            } else {
                $("#macthdir").hide();
            }
            ;
        });
        $("#logout").click(function () {
            var cookie = cz_cookie.createCookie();
            if (cookie.check('handle')) {
                cookie.del('handle');
                location.reload();
            }
        });
        $("#home").click(function(){
            if($("#username").text()!='handle'){
                $("#main-tab").slideDown();
            }
            $("#about-tab").slideUp();
        });
        $("#about").click(function(){
            $("#main-tab").slideUp();
            $("#about-tab").slideDown();
        });
    },
    plus: function(){
        var str = '<div class="control-group">'+
            '<label class="control-label" for="inputs">CNFG IP</label>'+
            '<div class="controls">'+
            '<abbr title="e.g.: 135.2.121.97" class="initialism"><input type="text" class="input-xlarge cnfg" name="labip"></abbr>'+
            '<div class="cnfgip" style="float: right; margin-top: 5px; margin-right: 160px;">'+
            '<a href="javascript:void(0)" class="ui-corner-all" role="button"><span class="ui-icon ui-icon-circle-minus">minus</span></a>'+
            '</div>'+
            '<p id="ip-tips" class="help-block" style="margin-top:0; font-size:12px;">Input the lab IP address.</p>'+
            '</div>'+
            '</div>';
        $("#bt-plus").click(function(){
            $("#labip").after(str);
        })
        $(".cnfgip").live('click',function(){
            $(this).parent('div').parent('div').remove();
        })
    }
}


