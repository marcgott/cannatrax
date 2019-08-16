$(document).ready(function() {
    console.log("script init")
            $(".logform").submit(function(event){
               event.preventDefault();
               //alert( "Default behavior is disabled!" );
               form_row_id = $(this).closest("form").attr('id')
               $(this).hide()
            });
         });
