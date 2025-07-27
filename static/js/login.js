  function updateTime() {
            const now = new Date();
            const time = now.toLocaleTimeString();
            const date = now.toLocaleDateString('zh-CN', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
            const weekday = now.toLocaleDateString('zh-CN', {
                weekday: 'long'
            });
            const fullDisplay = `${date} ${weekday} ${time}`;
            document.querySelector('.show-time').textContent = fullDisplay;
        }

  setInterval(updateTime, 1000);
  updateTime();

  function checkComplete(){
    const studentId = document.getElementsByName("username")[0];
    const password = document.getElementsByName("password")[0];

    if (!studentId.value || !password.value) {
        showAlert("请输入学号和密码", color="rgba(255, 0, 0, 1)");
        return;
    }
}

function checkAdmission(){
    const studentId = document.getElementsByName("username")[0];
    const password = document.getElementsByName("password")[0];

    if (!studentId.value) {
        showAlert("请输入学号", color="rgba(255, 0, 0, 1)");
        return;
    }

    fetch('/allowance', {
        method: 'post',
        body: JSON.stringify({
            username: studentId.value,
            password: password.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json())
      .then(data => {
          if (data.status === 'success') {
              showAlert("已授权用户");
              password.value = "";
          } else {
              showAlert("未授权用户", color="rgba(255, 0, 0, 1)");
          }
      });
}

function showAlert(message, color="rgba(87, 206, 82, 1)") {
    const container = document.getElementById("alert-container");
    const alertBox = document.createElement("div");

    alertBox.className = "alert alert-warning rounded fade-up";
    if (message === "已授权用户" || message === "登录成功！"){
        alertBox.innerHTML = `<i style="margin-right: 5px" class="fa fa-check-circle"></i>${message}`; // Bootstrap Icons
    } else {
        alertBox.innerHTML = `<i style="margin-right: 5px" class="fa fa-times-circle"></i>${message}`; // Bootstrap Icons
    }
    alertBox.style.background = color;
    alertBox.style.color = "#fff";
    alertBox.style.border = "none";
    alertBox.style.fontWeight = "bold";

    container.appendChild(alertBox);

    setTimeout(() => {
        container.removeChild(alertBox);
    }, 2000);
}