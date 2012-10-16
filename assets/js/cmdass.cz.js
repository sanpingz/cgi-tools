/**
 * Created with PyCharm.
 * User: sanpingz
 * Date: 12-8-15
 * Time: 下午1:31
 */
cz_command = {
    init : function () {
        $("#cmd-field").text('');
        $.getJSON('command.json', function (data) {
            var str = '';
            $(data.cmd).each(function (index, item) {
                str += '<option value="' + item.id + '" name="'+item.name+'">' + item.value + '</option>';
            })
            $("#command-select").append(str)
        });
    },
    change : function () {
        $("#command-select").change(function () {
            $("#cmd-field").text('');
            $("#option-field").empty();
            $("#gac").next('span').text('');
            var value = $(this).val();
            $("#cmd-description").hide();
            $("#cmd-text").text('');
            if (value != '') {
                $.getJSON('command.json', function (data) {
                    if (data.toString().length > 0) {
                        $(data.cmd).each(function(i,e){
                            if(value == e.id && e.hasOwnProperty('description') && e.description.length>0){
                                $("#cmd-text").text(e.description);
                                $("#cmd-description").show();
                                return false;
                            }
                        });
                    }
                });
                $.getJSON('parameter.json', function (data) {
                    if (data.toString().length > 0) {
                        var param = data.hasOwnProperty(value)?data[value]:{};
                        var doc = '';
                        for (var i = 0; i < param.length; i++) {
                            doc += cz_command.generate(param[i],i);
                        }
                        $("#option-field").append(doc);
                        $("#option-box").slideDown();
                    }
                });
            } else {
                $("#option-box").slideUp();
            }
        });
    },
    generate : function (param, index) {
        var type = param.type;
        var result = '';
        var flag = true;
        switch (type) {
            case 'hidden':
                result = handleHidden(index);
                flag = false;
                break;
            case 'text':
                result = handleText(index);
                break;
            case 'select':
                result = handleSelect(index);
                break;
            case 'checkbox':
                result = handleCheckbox(index);
                break;
            case 'radio':
                result = handleRadio(index);
                break;
            default :
                console.log("undefined type");
        }
        function handleHidden(index) {
            return '<input type="hidden" value="' + param.value + '" no="'+index+'">';
        }

        function handleText(index) {
            var cont = '';
            var rule = '';
            if (param.hasOwnProperty('rule') && param.rule.toString() == 'required') {
                cont = '<span class="text-tip">(*)</span>';
            }
            return '<label class="control-label">' + param.label + '</label>' +
                '<div class="controls">' +
                '<input type="text" name="' + param.name + '" value="'+ param.value +
                '" no="'+index+'" rule="'+param.rule+'">' +
                cont + '</div>';
        }

        function handleSelect(index) {
            var option = param.option;
            var cont = '';
            for (var i = 0; i < option.length; i++) {
                cont += '<option value="' + option[i].value + '">' + option[i].label + '</option>';
            }
            return '<label class="control-label">' + param.label + '</label>' +
                '<div class="controls"><select name="' + param.name + '" no="'+index+'">' + cont + '</select></div>';
        }

        function handleCheckbox(index) {
            return '<label class="control-label">' + param.label + '</label>' +
                '<div class="controls"><label class="checkbox">' +
                '<input type="checkbox" name="' + param.name + '" value="' + param.value + '" no="'+index+'"/>' +
                param.value + '</label></div>';
        }

        function handleRadio(index) {
            var input = param.input;
            var cont = '';
            for (var i = 0; i < input.length; i++) {
                var ck = (input[i].checked!=undefined&&input[i].checked)?'checked':'';
                cont += '<label class="radio">' +
                    '<input type="radio" name="' + param.name + '" value="' + input[i].value + '" ref="' + input[i].ref + '"'+ck+' no="'+index+'" />' +
                    input[i].label +'&nbsp;&nbsp;&nbsp;&nbsp;'+
                    '</label>';
            }
            return '<label class="control-label">' + param.label + '</label>' +
                '<div class="controls ctr-radio">' + cont + '</div>';
        }

        function wrapper(cont) {
            return '<div class="control-group group">' + cont + '</div>';
        }

        return (flag == true) ? wrapper(result) : result;
    },
    radio : function () {
        $("input[type=radio]").live('click', function () {
                $(this).parent('label').parent('div').find('input[type=text]').remove();
                if ($(this).attr('ref') == '@ref') {
                    $(this).parent('label').append('<input type="text" />');
                    $(this).parent('label').find('input[type=text]').first().focus();
                }
            }
        );
    },
    gac : function () {
        var cp = $("#cmd-field");
        String.prototype.trim = function() {
            return this.replace(/(^\s*)|(\s*$)/gm, '');
        }
        $("#gac").click(function () {
            var name = $("#command-select").val();
            var text = cz_command.parseValue().trim();
            if (name != '' && text!='') {
                cp.text(text);
                cz_command.copyToClipboard(text);
            }
        });
    },
    parseValue : function () {
        var field = $("#option-field");
        var selected = $("#command-select").find('option:selected');
        var cmd = selected.attr('name');
        var hidden = field.find('input[type=hidden]');
        var text = field.find('input[type=text]');
        var select = field.find('select');
        var checkbox = field.find('input[type=checkbox]');
        var radio = field.find('.ctr-radio');

        var array = new Array();
        var flag = true;
        if (hidden.length > 0) {
            $(hidden).each(function (i, e){
                array[$(e).attr('no')] = e.value;
            });
        }
        if (text.length > 0) {
            $(text).each(function (i, e) {
                if (e.name != '' && e.value != '') {
                    array[$(e).attr('no')] = e.name + ' ' + e.value;
                    text.parent('div').parent('div').removeClass( "warning" );
                }else if($(e).attr('rule') == 'required'){
                    $(e).parent('div').parent('div').addClass( "warning" );
                    flag = false;
                }
            });
        }
        if (select.length > 0) {
            $(select).each(function (i, e) {
                if (e.value != undefined && e.value != '') {
                    array[$(e).attr('no')] = e.name + ' ' + e.value;
                }
            });
        }
        if (checkbox.length > 0) {
            $(checkbox).each(function (i, e) {
                if (e.checked == true) {
                    array[$(e).attr('no')] = e.name + ' ' + e.value;
                }
            });
        }
        if (radio.length > 0) {
            $(radio).each(function (i, e) {
                var ro = $(e).find('input[type=radio]');
                $(ro).each(function (ii, ee) {
                    var refer = $(ee).attr('ref');
                    if (ee.checked && refer == '@ref') {
                        var ref = $(ee).parent('label').find('input[type=text]').first();
                        if (ref.val() != undefined && ref.val() != '') {
                            array[$(ee).attr('no')] = ee.value + ' ' + ref.val();
                        }
                    } else if (ee.checked && refer != '@ref') {
                        array[$(ee).attr('no')] = ee.value + ' ' + refer;
                    }
                });
            });
        }
        var str = cz_command.adapter(array);
        return (flag)?cmd+str:'';
    },
    adapter : function(array){
        var str = '';
        for(var i=0; i<array.length;i++){
            if(array[i]!=undefined && array[i]!=''){
                str += ' '+array[i];
            }
        }
        return str;
    },
    copyToClipboard : function (txt) {
        if(window.clipboardData) {
            window.clipboardData.setData("Text", txt);
            $("#gac").next('span').text('copied');
        }else{
            var text_area = document.getElementById("cmd-field");
            text_area.select();
            text_area.focus();
            $("#gac").next('span').text('selected');
        }
    }
}