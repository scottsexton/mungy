$(function() {
    //Attach Image select action
    $('#image_library img').click(function() {
        filename = $(this).attr('name');
        img1 = $('#munge_form input[name="image1"]').val();
        img2 = $('#munge_form input[name="image2"]').val();
        if(img1 == filename) {
            $('#munge_form input[name="image1"]').val('');
        } else if (img2 == filename) {
            $('#munge_form input[name="image2"]').val('');
        } else if(img1 == '') {
            $('#munge_form input[name="image1"]').val(filename);
        } else if(img2 == '') {
            $('#munge_form input[name="image2"]').val(filename);
        }
    });

    //Attach Validate action
    $('#munge_form').on('submit',function(e) {
        if($('#munge_form input[name=image1]').val() == '' || $('#munge_form input[name=image2]').val() == '') {
            alert('Please select two images.');
            return false;
        } else {
            return true;
        }
    });

    //Attach Delete action
    var deletor_xhr = null;
    var build_response_text = function(xhr) {
        return 'HTTP/1.1 ' + xhr.status + ' ' + xhr.statusText + '\n' + xhr.getAllResponseHeaders() + '\n' + xhr.responseText;
    };
    $('#deletor').submit(function(e) {
        e.preventDefault();
        if(deletor_xhr && deletor_xhr.readyState != 4) {
            deletor_xhr.abort();
        }
        var filename = $('#deletor input[name=filename]').val();
        if(filename) {
            filename = '/'+filename;
        }
        deletor_xhr = $.ajax({
            url: '/images'+filename,
            type: 'DELETE'
        });
        deletor_xhr.always(function() {
            console.log(build_response_text(deletor_xhr));
            location.href = '/';
        });
    });

    //Attach Delete click
    $('a.delete_link').click(function(e) {
        e.preventDefault();
        if(deletor_xhr && deletor_xhr.readyState != 4) {
            deletor_xhr.abort();
        }
        var filename = $(this).attr('href');
        deletor_xhr = $.ajax({
            url: '/images'+filename,
            type: 'DELETE'
        });
        deletor_xhr.always(function() {
            console.log(build_response_text(deletor_xhr));
            location.href = '/';
        });
    });
});
