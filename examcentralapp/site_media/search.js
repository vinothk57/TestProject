function search_submit() { 
  var query = $("#id_query").val();
  var query_string = "/search/?ajax&query=" + encodeURIComponent(query)
  var empty = 1;
  if (query.length === 0 || !query.trim()) {
    query_string = "/search/?ajax&query=" + encodeURIComponent(query) + "&blank=" + empty
  }
  $("#search-results").load(
    query_string
  );
  return false;
}

$(document).ready(function () {
  $("#search-form").submit(search_submit);
});
