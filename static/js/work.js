
    $(function(){
      $('.demo-contenteditable').pastableContenteditable();
      $('.demo').on('pasteImage', function(ev, data){
        var blobUrl = URL.createObjectURL(data.blob);
        var name = data.name != null ? ', name: ' + data.name : '';
        // console.log(data);
        var res = 'zero';
        var url = window.location.href + '/upload';
        $.ajax({
            url: url,
            type: 'POST',
            data:
                {
                    'data': data.dataURL
                },
            success: function (response) {
                // console.log(response);
                res = response.message;
                $('#message').text( "图片上传成功，转换结果：");
                $('#result').text(res);
                $('#btn').attr("data-clipboard-text",res);
            },
            error: function(responsestr){
                // console.log("error");
                // console.log(responsestr);
                $('#message').text( "上传失败，请重试！");
            }
        });
        $('#message').text( '图片正在上传,尺寸：' + data.width + ' x ' + data.height);
      })
    });
