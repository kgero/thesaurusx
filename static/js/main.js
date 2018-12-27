
function get_words_simple() {
  console.log('test');
  $('.results').empty();

  var data = {
    keyword: $('#keyword').val(),
    base: $('#base').val(),
    goal: $('#goal').val(),
    embd: $('input[name=embOptions]:checked').val()
  };
  console.log('get_words_simple().');
  console.log('data:', data);

  $.post('get_words_simple?', data, function(json, status) {
    console.log('response:', json);
    if (json.hasOwnProperty('error')) {
      $('.results').append('<p>' + json.error);
      return;
    }

    var words = json.words;
    $.each(words, function(i, text) {
      var p = $("<p>");
      p.append(text);
      $('.results').append(p);
    });
  });
}

$(document).ready( function() {

  console.log('booting up...');

  $('.get_words').click( function() { get_words_simple(); });

});
