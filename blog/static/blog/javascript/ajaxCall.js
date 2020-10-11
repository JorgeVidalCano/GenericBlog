// Search Bar
$(document).ready(function () {    
  var $myForm = $("#inputFormId")
  $myForm.keydown(function(event){

      var $formData = $(this).serialize();
      var $endpoint = window.location.origin + "/search/ajaxSearch"
      
    $.ajax({
      method: "GET",
      url: $endpoint,
      data: $formData,
      success: handleFormSuccess,
      error: handleFormError,
    })

    function handleFormSuccess(data, textStatus, jqXHR){

    var instance = JSON.parse(data["instance"]);
    $(".searchResult").remove();
    for ( var i = 0; i < instance.length; i++){      
      var results = $(`
                      <div class="container border p-1 searchResult">
                        <a href="/post/${instance[i].slug}" class="" /">
                          <div class="row top-buffer align-items-center flex-row-reverse">
                            <div class="col-lg-7 col-md-7 col-sm-12">
                              <div class="row about-list">
                                  <p>${instance[i].title}</p>
                              </div>
                            </div>
                            <div class="col-lg-5 col-md-5 align-items-center flex-row-reverse">
                                <img class="searchImg float-left" src="${instance[i].PostImages}">
                            </div>
                          </div>
                        </a>
                      </div>
        `);
      $(results).insertAfter("#inputFormId");
      }
    }
    function handleFormError(data, textStatus, errorThrown){
      console.log(data)
      console.log(textStatus)
      console.log(errorThrown)
    }
  })
  }
)

$(document).ready(function () {
  $("#inputFormId").focusout(function() {
    // deletes the search if focus is lost
    setTimeout(function() { 
      $(".searchResult").remove();
    }, 200); 
  });
})

//////////////////////////////////////////////////////////////////////////////////////////////

// Loads new posts when the bottom is near.
$(document).ready(function () {
  var c = 1;
  let end = false
  let call = true;
  
  $(window).on("scroll", function(){
    
    if(call == true){
    if( $(this).scrollTop() > ($(document).height()*0.65).toFixed(0) & end == false) {
      call = false;
      c ++
      var $formData = $(this).serialize();
      var $endpoint = window.location.origin + "/search/ajaxCall/" + c + window.location.href.slice(window.location.origin.length, -1)
          
      $.ajax({
        method: "GET",
        url: $endpoint,
        data: $formData,
        success: handleFormSuccess,
        error: handleFormError,
      })

      function handleFormSuccess(data, textStatus, jqXHR){

      var instance = JSON.parse(data["instance"]);
      
      end = JSON.parse(data["end"]);
      
      for ( var i = 0; i < instance.length; i++){      
        var tags ='';
        $.each(instance[i].tags, function(index, v){
          tags += `<span class="badge badge-warning">${v}</span>`
        });
        
        var results = $(`
                        <div class="card mb-4">
                          <img class="border card-img-top" src="${ instance[i].image }" alt="Card image cap">
                          <div class="card-body">
                              <h2 class="card-title">${ instance[i].title }</h2>
                              ${tags}
                              <hr>
                              <p class="card-text">${ instance[i].content.split(/\s+/).slice(0,35).join(" ") }</p>
                              <a href="/post/${ instance[i].slug }" class="btn btn-primary">Read More &rarr;</a>
                          </div>
                          <div class="card-footer text-muted">
                          Posted on ${ instance[i].datePosted } by <span class="text-primary">@${ instance[i].author }</span>
                          </div>
                        </div>
          `);
      $(".col-md-8").append( $(results));
      }
      call=true
      
      }
      function handleFormError(data, textStatus, errorThrown){
        console.log(data)
        console.log(textStatus)
        console.log(errorThrown)
      }
    }}
  }
  )
})

// Subscribe and unsubscriber mailchimp
$(document).ready(function () {
  var $myForm = $("#mailChimpSubs")
  $myForm.submit(function(event){
    event.preventDefault();
    var $formData = $(this).serialize();
    var $endpoint = $myForm.attr("data-url") || window.location.href
    $.ajax({
      method: "POST",
      url: $endpoint + "subscribe/",
      data: $formData,
      success: handleFormSuccess,
      error: handleFormError,
    })

  function handleFormSuccess(data, textStatus, jqXHR){
    alert(data["instance"]);
  }
  function handleFormError(data, textStatus, errorThrown){
    console.log(data)
    console.log(textStatus)
    console.log(errorThrown)
  }
 })
 }
)