// 渲染日志的函数
function renderLogs(logs) {
    $('#log-list').empty();  // 清空现有日志列表
    logs.forEach(function (log) {
        $('#log-list').append(
            `<tr>
                <td>${log.operation_id}</td>
                <td>${log.operationtime}</td>
                <td>${log.membername}</td>
                <td>${log.membertelphone}</td>
                <td>${log.operationitem}</td>
                <td>
                <span class="operation-request"  title="${log.operationrequest}">
                ${log.operationrequest}
                </span>
                </td>
            </tr>`
        );
    });
}

// 搜索和分页请求的函数
function searchLogs(page = 1) {
    // 获取输入框中的查询内容
    const starttime = $('#start-date').val();
    const endtime = $('#end-date').val();
    const logname = $('#log-name').val();
    const logphone = $('#log-phone').val();


    $.ajax({
        url: '/operation-log/',
        type: 'GET',
        data: {
            starttime: starttime,
            endtime: endtime,
            logname: logname,
            logphone: logphone,
            page: page,  // 当前页码
            page_size: 10
        },
        success: function (response) {
            var logs = response.logs;
            var totalPages = response.total_pages;
            // 渲染日志
            renderLogs(logs);
            renderPagination(page, totalPages);
        },
        error: function (response) {
            alert(response.message);
        }
    });
}

// 优化按钮脚本   // 分页渲染函数，首次加载和查询结果都可以使用这个函数
function renderPagination(page, totalPages) {
    const $pagination = $('#pagination');
    var current_page = page

    // 清空分页组件内容
    $pagination.empty();

    // 添加首页和上一页按钮
    $pagination.append(`
        <li class="page-item" id="first-page">
            <a class="page-link" href="#" tabindex="-1" aria-disabled="true">首页</a>
        </li>
        <li class="page-item" id="prev-page">
            <a class="page-link" href="#" tabindex="-1" aria-disabled="true">&laquo;</a>
        </li>
    `);

    // 动态添加页码按钮
    for (let i = 1; i <= totalPages; i++) {
        $pagination.append(`
            <li class="page-item ${i === current_page ? 'active' : ''}"><a class="page-link" href="#">${i}</a></li>
        `);
    }

    // 添加下一页和末页按钮
    $pagination.append(`
        <li class="page-item" id="next-page">
            <a class="page-link" href="#">&raquo;</a>
        </li>
        <li class="page-item" id="last-page">
            <a class="page-link" href="#">末页</a>
        </li>
    `);
    // 更新上一页和下一页按钮的状态
    if (current_page <= 1) {
        $('#first-page, #prev-page').addClass('disabled').attr('aria-disabled', 'true');
    } else {
        $('#first-page, #prev-page').removeClass('disabled').attr('aria-disabled', 'false');
    }

    if (current_page >= totalPages) {
        $('#next-page, #last-page').addClass('disabled').attr('aria-disabled', 'true');
    } else {
        $('#next-page, #last-page').removeClass('disabled').attr('aria-disabled', 'false');
    }

    // 重新绑定分页按钮的点击事件
    $('.page-link').on('click', function (event) {
        event.preventDefault(); // 阻止默认链接行为
        if ($(this).parent().hasClass('disabled')) {
            return;
        } // 如果按钮是禁用状态，则不处理点击事件
        let clickedPage = $(this).text().trim();
        let currentPageText = $('.page-item.active').text().trim();
        let currentPage = !isNaN(currentPageText) ? parseInt(currentPageText) : 1;

        if (clickedPage === "首页") {
            goToPage(1, totalPages);
        } else if (clickedPage === "末页") {
            goToPage(totalPages, totalPages);
        } else if (clickedPage === "«" && currentPage > 1) {
            goToPage(parseInt(currentPage) - 1, totalPages);
        } else if (clickedPage === "»" && currentPage < totalPages) {

            goToPage(parseInt(currentPage) + 1, totalPages);
        } else {
            goToPage(parseInt(clickedPage), totalPages);
        }
    });
}

function goToPage(pageNumber, totalPages) {
    // 假设有一个 totalPages，全局设置为最新获取的分页总数
    if (pageNumber < 1 || pageNumber > totalPages) {
        return;
    }
    var $page_item = $('.page-item')

    // 设置新的激活页码
    $page_item.removeClass('active');
    $page_item.each(function () {
        var pageNumber_temp = Number($(this).find('a').text().trim())
        if (!isNaN(pageNumber_temp) && pageNumber_temp === pageNumber) {
            $(this).addClass('active');
        }
    });

    // 加载该页的数据
    searchLogs(pageNumber);
}

// 首次加载时直接渲染日志和分页
$(document).ready(function () {
    searchLogs();  // 默认加载第一页
});

// 点击按钮后要阻止刷新页面
$('#btn-search').click(function (event) {
    event.preventDefault()
    searchLogs()
})