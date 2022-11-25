$(document).ready(function () {
  $(".filter-checkbox").on("click", function () {
    var filter_object = {};
    $(".filter-checkbox").each(function (index, ele) {
      var filter_value = $(this).val();
      var filter_key = $(this).data("filter");
      console.log(filter_key, filter_value);
      filter_object[filter_key] = Array.from(
        document.querySelectorAll(
          "input[data-filter=" + filter_key + "]:checked"
        )
      ).map(function (el) {
        return el.value;
      });
    });
    $.ajax({
      url: "product/filter-data",
      data: filter_object,
      dataType: "json",
      success: function (res) {
        $("#filteredProducts").html(res.data);
      },
    });
  });
});
console.log("hello world");
