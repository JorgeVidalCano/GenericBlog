// Adds comments 
$(document).ready(function () {
  var $myForm = $("#comment_form_id")
  $myForm.submit(function(event){
    event.preventDefault();
    var $formData = $(this).serialize();
    var $endpoint = $myForm.attr("data-url") || window.location.href
    //alert($formData)
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
      
      var comment = $(`
      <div class="media mb-4 comment">
        <div class="imgProfileContainer">
            <img class="imgProfile" src="${data["img"]}" alt="${ data["name"] }">
        </div>
        <div class="media-body">
        <h5 class="mt-0">@${data["name"]}</h5>
        <small class="small">now</small>
            <div class="card">
                ${fields["comment"]}
            </div>
        </div>
      </div>
    `).hide();
    $("#comments").prepend(comment);
    comment.fadeIn(800);
    }
    function handleFormError(data, textStatus, errorThrown){
      console.log(data)
      console.log(textStatus)
      console.log(errorThrown)
    }
  })
  }
)

// Update comments 
$(document).ready(function () {
  var $clickButton = $(".updateComment")
  $clickButton.click(function(event){
    event.preventDefault();
    var $formData = ($(this).parent());
    var $endpoint = this;
    $formData = $formData.serialize()
    
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
    }
    function handleFormError(data, textStatus, errorThrown){
      console.log(data)
      console.log(textStatus)
      console.log(errorThrown)
    }
  })
  }
)

// Delete comments 
$(document).ready(function () {
  var $clickButton = $(".deleteComment")
  $clickButton.click(function(event){
    event.preventDefault();
    var $form = $(this).parent();
    var $endpoint = this
    $formData = $form.serialize()
    
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
      
      $form.parent().parent().fadeOut(400, "linear");
    }
    function handleFormError(data, textStatus, errorThrown){
      console.log(data)
      console.log(textStatus)
      console.log(errorThrown)
    }
  })
  }
)

//show the update and delete buttons for comments
$(document).ready(function(){
  var $commentArea = $(".media.mb-4.comment")
  $commentArea.hover(function(event){
    $(this).find("a").show();
  })
  $commentArea.mouseleave(function(event){
    $(this).find("a").hide();
  })
}
)

// Adds likes 
$(document).ready(function () {
  var $opinion = $(".likesPost")
  var $opinionSelected = ""
  $opinion.click(function(event){

    event.preventDefault();
    var $endpoint = $(this).attr("data-ref")    
    var $opinion = this.value;
  
    $.ajax({
      method: "POST",
      url: $endpoint,
      data: {'value': $opinion},
      success: handleFormSuccess,
      error: handleFormError,
    })
    function handleFormSuccess(data, textStatus, jqXHR){
      console.log(textStatus)
      console.log(jqXHR)
      
      if ($opinion == "like" & $opinionSelected != "like"){
        $(".text-primary")[0].innerHTML = parseInt($(".text-primary")[0].innerHTML) + 1;
        if($opinionSelected == "unlike"){
          $(".text-alert")[0].innerHTML = parseInt($(".text-alert")[0].innerHTML) - 1;
        }
      }else if ($opinion == "unlike" & $opinionSelected != "unlike"){
        $(".text-alert")[0].innerHTML = parseInt($(".text-alert")[0].innerHTML) + 1;
        if($opinionSelected == "like"){
          $(".text-primary")[0].innerHTML = parseInt($(".text-primary")[0].innerHTML) - 1;
        }
      }
      $opinionSelected = $opinion
    }
    function handleFormError(data, textStatus, errorThrown){
      console.log(data)
      console.log(textStatus)
      console.log(errorThrown)
    }
  })
  }
)
  
// Admin panel.
// Submits the publish button in /post/myposts
// Publish post 
$(document).ready(function () {
  
  var $myForm = $("#publish_post_form");
  
  $("#tableContent tr").click(function(){      
    var tablaData = $(this).children("td").map(function(){
      return $(this).text();
    }).get();
    $slug = $('.' + tablaData[5] + "Slug").val();
    $publishValue = $('.' + tablaData[5] + "Publish").val();    
  })
        
    $myForm.submit(function (event) {
    event.preventDefault();
    var $csfr = $("input").val();
    var $formData = "csrfmiddlewaretoken="+$csfr+"&slugPost="+$slug+"&publishPost="+$publishValue //whyyy!!
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
      
      if ($publishValue.toLowerCase() == 'true'){
        $newState = 'unpublished';
        $newValue = false;
      }else{
        $newState = 'published';
        $newValue = true
      }
      $('.' + $slug + "Publish").val($newValue); // updates the new val()
      var sucessAnswer = $(
        `<div id="alert" class="alert alert-success alert-dismissible fade show position-absolute">
          <button type="button" class="close" data-dismiss="alert">&times;</button>
          ${data['instance'] + $newState}
        </div>`
        ).hide();
        $("#head").append(sucessAnswer)
      
        sucessAnswer.fadeIn(300);
        setTimeout(function() { 
            $('#alert').remove(); 
        }, 4000);        
      }

      function handleFormError(data, textStatus, errorThrown){
        console.log(data)
        console.log(textStatus)
        console.log(errorThrown)
      }
  })
})

// Adds favorite
$(document).ready(function () {
  var $opinion = $("#fav_button")
  $opinion.click(function(event){
    
    event.preventDefault();
    var $endpoint = $(this).attr("data-ref")    
    var $opinion = $("#favorite").val();
        
    $.ajax({
      method: "POST",
      url: $endpoint,
      data: {'value': $opinion},
      success: handleFormSuccess,
      error: handleFormError,
    })

    function handleFormSuccess(data, textStatus, jqXHR){
      console.log(textStatus)
      console.log(jqXHR)
      
      if ($opinion == "True"){
        $("#favorite").val("False")
        $("#spanFav").text("Add to favorite")
        var successAnswer = $(`<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-star-fill" fill="gold" xmlns="http://www.w3.org/2000/svg">
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.283.95l-3.523 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
                              </svg>`
                              )
      }else{
        $("#favorite").val("True")
        $("#spanFav").text("Remove from favorite")
        var successAnswer = $(`<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-star" fill="gold" xmlns="http://www.w3.org/2000/svg">
                                <path fill-rule="evenodd" d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.523-3.356c.329-.314.158-.888-.283-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767l-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288l1.847-3.658 1.846 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.564.564 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"/>
                              </svg>`
                              )
      }
      $("#fav_button>svg").replaceWith(successAnswer)
    }
    function handleFormError(data, textStatus, errorThrown){
      console.log(data)
      console.log(textStatus)
      console.log(errorThrown)
    }
  })
  }
)

// Remove favs in the user's profile
$(document).ready(function () {
  var $myForm = $("#publish_post_form_fav")

  $("#tableContentFav tr").click(function(){      
    var tablaData = $(this).children("td").map(function(){
      return $(this).text();
    }).get();
    $slug = tablaData[1].replace(/\s+/g, "-");   
  })
  $myForm.submit(function(event){
    event.preventDefault();
    var $formData = $(this).serialize();
    var $endpoint = $slug + "/favorite"
    
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
      
      var instance = data["instance"];
      var row = $("." + instance)
      row.fadeOut()
    }
    function handleFormError(data, textStatus, errorThrown){
      console.log(data)
      console.log(textStatus)
      console.log(errorThrown)
    }
  })
  }
)
