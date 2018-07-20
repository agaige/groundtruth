// custom javascript

$( document ).ready(() => {
  console.log('Sanity Check!');
});

$('.btn').on('click', function() {
  $.ajax({
    url: '/tasks',
    data: { url: $('#input-url').val() },
    method: 'POST'
  })
  .done((res) => {
    getStatus(res.data.task_id)
  })
  .fail((err) => {
    console.log(err)
  });
});

function getStatus(taskID) {
  $.ajax({
    url: `/tasks/${taskID}`,
    method: 'GET'
  })
  .done((res) => {
    const html = `
      <tr>
        <td>${res.data.task_id}</td>
        <td>${res.data.task_status}</td>
        <td>${res.data.task_result}</td>
      </tr>`
    $('#tasks').prepend(html);
    const taskStatus = res.data.task_status;
    if (taskStatus === 'finished') {
      var elem = document.getElementById("output-image")
      if (elem != null) {
        elem.setAttribute("src", `${res.data.task_result}`);
        return false;
      }
      elem = document.createElement("img");
      elem.setAttribute("id", "output-image")
      elem.setAttribute("src", `${res.data.task_result['value']}`);
      elem.setAttribute("height", "1024");
      elem.setAttribute("width", "1024");
      document.getElementById("output-container").appendChild(elem);
      return false;
    } else if (taskStatus === 'failed') {
        return false;
    }

    setTimeout(function() {
      getStatus(res.data.task_id);
    }, 2000);
  })
  .fail((err) => {
    console.log(err)
  });
}
