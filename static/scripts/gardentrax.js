$(document).ready(function() {
            $(".logform").submit(function(event){
               event.preventDefault();
               //alert( "Default behavior is disabled!" );
               form_row_id = $(this).closest("form").attr('id')
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
              $('.environmentfield').val($(this).val());
            });
            $('#global_nutrient_ID').on('change',function(){
              $('.nutrientfield').val($(this).val());
            });
            $('#global_repellent_ID').on('change',function(){
              $('.repellentfield').val($(this).val());
            });
            $('#global_stage').on('change',function(){
              $('.stagefield').val($(this).val());
            });
         });
