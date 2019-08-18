$(document).ready(function() {
    console.log("script init")
            $(".logform").submit(function(event){
               event.preventDefault();
               //alert( "Default behavior is disabled!" );
               form_row_id = $(this).closest("form").attr('id')
               console.log($("#"+form_row_id))
               $.post("/log/new",$("#"+form_row_id).serialize(),function(data){
                 $("#"+form_row_id).hide()
               })
               //
            });
            $( function() {
              $( ".datefield" ).datepicker({dateFormat: 'yy-mm-dd'});
            } );
            $('#globaldate').click(function(){
              $('#globaldatefield').datepicker('show');
            });
            $('#globaldatefield').datepicker({dateFormat: 'yy-mm-dd', onSelect:
              function(dateText, inst) {
                $('.datefield').val(dateText);
              }
            });
            $('#globalwater').click(function(){
              $('.watercheck').prop('checked',true);
            });
            $('#global_environment_ID').on('change',function(){
              console.log($(this))
              $('.environmentfield').val($(this).val());
            });
            $('#global_nutrient_ID').on('change',function(){
              console.log($(this))
              $('.nutrientfield').val($(this).val());
            });
            $('#global_repellent_ID').on('change',function(){
              console.log($(this))
              $('.repellentfield').val($(this).val());
            });
            $('#global_stage').on('change',function(){
              console.log($(this))
              $('.stagefield').val($(this).val());
            });
         });
