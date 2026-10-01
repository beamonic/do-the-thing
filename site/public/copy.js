document.querySelectorAll('button.copy').forEach(function (button) {
  var label = button.dataset.label || 'Copy';
  var doneLabel = button.dataset.done || 'Copied';
  var failLabel = button.dataset.fail || 'Select and copy';
  button.addEventListener('click', function () {
    var text = document.querySelector(button.dataset.copy).textContent;
    var done = function () {
      button.textContent = doneLabel;
      setTimeout(function () { button.textContent = label; }, 1600);
    };
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(done, function () { button.textContent = failLabel; });
    } else {
      button.textContent = failLabel;
    }
  });
});
