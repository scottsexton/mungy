<div id="image_library">
%for img in images:
<div class="uploaded_image">
    <img src='/images/{{img.filename}}' name='{{img.filename}}'><br>
    <div class="delete_link"><a class="delete_link" href="/{{img.filename}}">[X]</a></div><div class="lefty">{{img.filename}}</div>
</div>
%end
</div>

<div id="form_column">
<form id="upload_form" method="POST" action="/images" enctype='multipart/form-data'>
    Upload an image of your own:<br>
    <input type="file" name="new_upload"><br>
    <input type="submit">
</form>

<br><br><br>

<form id="deletor">
    Delete image by name (empty for all):<br>
    <input type="text" name="filename">
    <input type="submit" value="Delete">
</form>

<br><br><br>

<form id="munge_form" method="POST" action="/munge">
    Select two images to munge:<br>
    Image 1:<input type="text" name="image1"><br>
    Image 2:<input type="text" name="image2"><br>
    Select a munging algorithm:<br>
    <select name="algorithm">
        <option value="ManipBlend">Blend</option>
        <option value="ManipCompose">Compose</option>
    </select>
    <input type="submit">
</form>
</div>

%rebase boilerplate
