$(function () {

  $("#create-app-btn").click(function(){
    var app_name = $('#app_name').val();
    var description = $('#description').val();
    var app_usage = $('#app-situation').val();

    $.ajax({
        type : "POST",  //提交方式
        url : "/app/create",//路径
        data : {
            "app_name"      :   app_name,
            "description"   :   description,
            "app_usage"     :   app_usage
        },
        success : function(result) {//返回数据根据结果进行相应的处理
            if ( result.status == 200 ) {
                window.location.href = "/app/list";
            } else {
                if ( result.status == 400 ){
                    $('#warning-div').show();
                    $('#warning-span').text('输入不得为空');
                } else if ( result.status == 401 ){
                    $('#warning-div').show();
                    $('#warning-span').text('app命名已存在');
                }
            }
        }
    });
  });


  $('#signup-btn').click(function(){

    $('#warning-tip').val('');
    $('#warning-div').hide();

    var username = $('#username').val();
    var password = $('#password').val();
    var repassword = $('#repassword').val();
    var email = $('#email').val();

    $.ajax({
        type : "POST",
        url  : "/signup",
        data : {
            "username"   :  username,
            "password"   :  password,
            "repassword" :  repassword,
            "email"      :  email
        },
        success : function(result) {

            if (result.status == 200){
                window.location.href = "/signin"
            } else {
                if(result.status == 401){
                    $('#warning-div').show();
                    $('#warning-tip').text('输入不得为空');
                }
                else if (result.status == 402) {
                    $('#warning-div').show();
                    $('#warning-tip').text('密码输入不一致');
                }
            }
        }
    });

  });


  $('#search-input').bind('keypress',function(event){
    if(event.keyCode == 13){
//        alert('test');
        var txt = $(this).val();
        window.location.href = "/app/search?content="+txt;
    }
  });


  $('#app-situation').change(function(){
    $('#app-situation').text($(this).val())
  });


  $('#signin-btn').click(function(){

    $('#warning-tip').val('');
    $('#warning-div').hide();

    var email = $('#email').val();
    var password = $('#password').val();

    $.ajax({
        type : "POST",
        url  : "/signin",
        data : {
            "email"      :  email,
            "password"   :  password
        },
        success : function(result) {
            if (result.status == 200){
                window.location.href = "/app/list"
            } else {
                if(result.status == 401){
                    $('#warning-div').show();
                    $('#warning-tip').text('输入不得为空');
                } else if(result.status == 402){
                    $('#warning-div').show();
                    $('#warning-tip').text('用户名或密码错误');
                } else if(result.status == 403){
                    $('#warning-div').show();
                    $('#warning-tip').text('用户名或邮箱已注册');
                }
            }
        }
    });

  });


  $('#modify-password-btn').click(function(){

    var new_password = $('#new_password').val();
    var old_password = $('#old_password').val();
    var confirm_password = $('#confirm_password').val();
//
//    alert(new_password);
//    alert(old_password);
//    alert(confirm_password);

    if(new_password == '' || old_password == '' || confirm_password == ''){
        $('#warning-div').show();
        $('#warning-tip').text('输入不得为空');
        return;
    }

    if(new_password != confirm_password){
        $('#warning-div').show();
        $('#warning-tip').text('两次输入密码不一致');
        return;
    }

    $.ajax({
        type: "POST",
        url: "/user/modify",
        data: {
            "new_password" : new_password,
            "old_password" : old_password,
            "confirm_password" : confirm_password
        },
        success : function(result) {
             if (result.status == 200){
                window.location.href = "/app/list"
            } else {
                if (result.status == 400){
                    $('#warning-div').show();
                    $('#warning-tip').text('输入不得为空');
                } else if(result.status == 401){
                    $('#warning-div').show();
                    $('#warning-tip').text('两次输入密码不一致');
                } else if(result.status == 402){
                    $('#warning-div').show();
                    $('#warning-tip').text('密码输入错误');
                } else if(result.status == 403){
                    $('#warning-div').show();
                    $('#warning-tip').text('修改错误');
                }
            }
        }
    });

  });


  $('#edit-info-submit-btn').click(function(){

    var nickname = $('#nickname').val();
    var sex = $('#sex').val();
    var school = $('#school').val();
    var degree = $('#degree').val();
    var qq = $('#qq').val();
    var weibo = $('#weibo').val();
    var github = $('#github').val();
    var info = $('#info').val();
    var hobby = $('#hobby').val();
    var phone = $('#phone').val();

    $.ajax({
        type: "POST",
        url: "/user/edit",
        data:{
            "nickname" : nickname,
            "sex" : sex,
            "school" : school,
            "degree" : degree,
            "qq" : qq,
            "weibo" : weibo,
            "github" : github,
            "info" : info,
            "hobby" : hobby,
            'phone' : phone
        },
        success : function(result) {
            if(result.status == 200){
                window.location.href = "/user/info"
            }
        }

    });


  });


 });


 function clear_input() {
    $('#app_name').text('');
    $('#description').text('');
    $('#company').text('');
 }
