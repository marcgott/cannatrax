$(document).ready(function() {
            $(".logform").submit(function(event){
               event.preventDefault();
               //alert( "Default behavior is disabled!" );
               form_row_action = $(this).closest("form").attr('action')
               form_row_id = $(this).closest("form").attr('id')
               $.post(form_row_action,$("#"+form_row_id).serialize(),function(data){
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

    $(".reportlink").click(function(){
      $(".report.chart").hide()
      $("#chart_"+$(this).attr('id')).show()
    })
    //Autosets logdate in /log/new, ignored in /log/edit/# and other
    if(typeof $('.datefield').val() != 'undefined' && $('.datefield').val() =='' ){
      date = new Date()
      isodate = date.toISOString().split('T')
      $('.datefield').val(isodate[0]);
    }

});
