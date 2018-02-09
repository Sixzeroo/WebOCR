    function addDiv(res) {
        $('<div class="ui segment">' +res+ '</div>').insertAfter($('#tar'));
    }

    $(function(){
      $('.demo-contenteditable').pastableContenteditable();
      $('.demo').on('pasteImage', function(ev, data){
        var blobUrl = URL.createObjectURL(data.blob);
        var name = data.name != null ? ', name: ' + data.name : '';
        console.log(data);
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
                console.log(response);
                res = response.message;
                addDiv(res);
                addDiv("结果：")
            },
            error: function(responsestr){
                console.log("error");
                console.log(responsestr);
            }
        });
        $('<div class="ui segment">' + data.width + ' x ' + data.height + '图片正在上传' + '</div>').insertAfter(this);
      })
    });