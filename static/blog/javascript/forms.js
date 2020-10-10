// Changes spaces to - to the title
document.getElementById("id_title").addEventListener('keyup', fillSlugField);

function fillSlugField() {
var slug = document.getElementById("id_title").value.replace(/\s+/g, "-");
  document.getElementById("id_slug").value = slug;
}

// Styles the tag's checkboxes 
$(function () {
    $( "#id_tags" )
    .change(function () {
      $( ".checkbox-tag" ).each(function() {
        label = $("label[for=" + $(this).attr('id') +"]")
        if ($(this).is(":checked")){
          label.addClass("badge badge-warning")
        }else{  
          label.removeClass("badge badge-warning")
        };
    })
  })
    .change();
});

