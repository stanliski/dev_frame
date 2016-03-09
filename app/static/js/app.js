$(function () {

  $("#create-app-btn").click(function(){
    var app_name = $('#app_name').val();
    var description = $('#description').val();
    var company = $('#company').val();

    $.ajax({
        type : "POST",  //提交方式
        url : "/app/create",//路径
        data : {
            "app_name"      : app_name,
            "description"   : description,
            "company"       : company
        },
        success : function(result) {//返回数据根据结果进行相应的处理
            if ( result.status == 200 ) {
                window.location.href = "/app/list";
            } else {
//                alert('添加失败!');
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
                window.location.href = "/app/list"
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
                } else if(result.status == 403){
                    $('#warning-div').show();
                    $('#warning-tip').text('用户名或密码错误');
                }
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
