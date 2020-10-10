// Adds Tags
$(document).ready(function () {
    
    var $myForm = $(".form-signin")
    $myForm.submit(function(event){
      event.preventDefault();
      var $formData = $(this).serialize();
      var $endpoint = $myForm.attr("data-url") || window.location.href
      
      $.ajax({
        method: "POST",
        url: $endpoint,
        data: $formData,
        success: handleFormSuccess,
        error: handleFormError,
      })
      
      function handleFormSuccess(data, textStatus, jqXHR){
        console.log(data)
        console.log(textStatus)
        console.log(jqXHR)
        $myForm[0].reset();
        
        var instance = JSON.parse(data["instance"]);
        var fields = instance[0]["fields"];
        
        var tag = $(`
            <div class="col-lg-2 col-md-2 col-sm-2">
            <ul class="list-unstyled mb-0">
                <li>
                    <span class="badge badge-warning">${fields["tag"]}</span>
                </li>
            </ul>
        </div>

        `).hide();
        $("#rowTag").prepend(tag);
        tag.fadeIn(800); 
      }

      function handleFormError(data, textStatus, errorThrown){
        console.log(data)
        console.log(textStatus)
        console.log(errorThrown)
        alert("Tag Repeated")

      }
    })
    }
  )