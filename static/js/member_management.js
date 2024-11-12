// 查询会员事件处理
function searchMembers(page = 1) {
// 在这里执行会员查询逻辑
// 如果没有查询条件，按照数据库的默认排序返回所有会员
// 每页显示10条数据，支持翻页
    const name = $('#search-name').val();
    const phone = $('#search-phone').val();
    // AJAX 请求查询你后端会员数据
    $.ajax({
        url:'/member-management/',
        method: 'GET',
        data:{
            name:name,
            phone:phone,
            page:page,
            page_size:10
        },
        success: function (response) {
            // 清空现有的会员列表
            $('#member-list').empty();

            // 渲染会员数据
            response.members.forEach(function (member) {
                $('#member-list').append(`
                <tr id="member-row-${member.member_id}">
                    <td class="member-id">${member.member_id}</td>
                    <td class="member-name">${member.membername}</td>
                    <td class="member-phone">${member.membertelphone}</td>
                    <td class="member-purchase-count">${member.memberpurchasecount}</td>
                    <td class="member-remaining-count">${member.memberremaincount}</td>
                    <td>
                        <button class="btn btn-primary btn-sm" onclick="showEditMemberModal('${member.member_id}')">编辑</button>
                        <button class="btn btn-primary btn-sm" onclick="showBuyMemberModal('${member.member_id}')">购买</button>
                    </td>
                </tr>
                `);
                // 渲染分页
            if (response.total_pages){
                renderPagination(page,response.total_pages) }
            })
        },
        error: function (error) {
            alert('查询会员信息出错，请稍后再试')
        }
    })
}

function renderPagination(page,totalPages) {
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
            return;} // 如果按钮是禁用状态，则不处理点击事件
        let clickedPage = $(this).text().trim();
        let currentPageText = $('.page-item.active').text().trim();
        let currentPage = !isNaN(currentPageText) ? parseInt(currentPageText) : 1;

        if (clickedPage === "首页") {
            goToPage(1,totalPages);
        } else if (clickedPage === "末页") {
            goToPage(totalPages,totalPages);
        } else if (clickedPage === "«" && currentPage > 1) {
            goToPage(parseInt(currentPage) - 1,totalPages);
        } else if (clickedPage === "»" && currentPage < totalPages) {
            goToPage(parseInt(currentPage) + 1,totalPages);
        } else {
            goToPage(parseInt(clickedPage),totalPages);
        }
    });
}

function goToPage(pageNumber,totalPages) {
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
    searchMembers(pageNumber);
}

 // 首次加载同点击查询显示前10条并支持分页
$(document).ready(function(){
    searchMembers();
})

$('#search-member-button').click(function(event) {
    event.preventDefault()
// 查询按钮点击后重新渲染分页组件和数据
    searchMembers();
});


 // 显示新增会员模态框
function showAddMemberModal() {
    document.getElementById('addMemberModal').style.display = 'flex';
    $('#addMemberModal input').val('')
}

// 关闭新增会员模态框
function closeAddMemberModal() {
    document.getElementById('addMemberModal').style.display = 'none';
}
    // 获取 CSRF 令牌
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// 保存新增会员信息
function addMember() {
    // 获取表单数据
    const name = document.getElementById('name').value;
    const phone = document.getElementById('phone').value;
    const purchaseCount = parseInt(document.getElementById('purchaseCount').value);
    const remainingCount = parseInt(document.getElementById('remainingCount').value);
    // 正则验证姓名是否包含特殊字符
    const namePattern = /^[\u4e00-\u9fa5a-zA-Z ]+$/;
    if (!namePattern.test(name)) {
        alert('姓名不能包含特殊字符，只能包含中文、英文字母和空格');
        return;
    }

    // 验证电话是否为纯数字
    const phonePattern = /^\d+$/;
    if (!phonePattern.test(phone)) {
        alert('电话只能包含数字');
        return;
    }

    // 验证购买次数是否为正整数
    if (purchaseCount <= 0 || isNaN(purchaseCount)) {
        alert('购买次数必须是正整数');
        return;
    }

    // 验证剩余次数是否为正整数且不超过购买次数
    if (remainingCount <= 0 || isNaN(remainingCount)) {
        alert('剩余次数必须是正整数');
        return;
    }

    if (remainingCount > purchaseCount) {
        alert('剩余次数不能超过购买次数');
        return;
    }

    // 简单的表单验证
    if (!name || !phone || !purchaseCount || !remainingCount) {
        alert('请填写所有字段');
        return;
    }
      // 通过 AJAX 向后端接口发送数据
    $.ajax({
        url: '/member-management/',  // /member-management/
        method: 'POST',
        contentType: 'application/json',
        headers: {'X-CSRFToken': getCSRFToken() },  // csrftoken 是你的 CSRF 令牌变量
        data: JSON.stringify({
            name: name,
            phone: phone,
            purchase_count: parseInt(purchaseCount),
            remaining_count: parseInt(remainingCount)
        }),
        success: function (response) {
            // 后端接口调用成功的回调处理
            alert('会员新增成功');
            closeAddMemberModal();
            location.reload();  // 重新加载页面以显示新增会员
        },
        error: function (xhr, status, error) {
            // 后端接口调用失败的回调处理
            alert('新增会员时出错，请稍后再试');
        }
    });
}

// 显示编辑会员模态框
function showEditMemberModal(memberId) {
    const row = document.querySelector(`#member-row-${memberId}`);
    const name = row.querySelector('.member-name').innerText;
    const phone = row.querySelector('.member-phone').innerText;
    const purchaseCount = row.querySelector('.member-purchase-count').innerText;
    const remainingCount = row.querySelector('.member-remaining-count').innerText;

    // 将数据填充到模态框表单中
    document.getElementById('editName').value = name;
    document.getElementById('editPhone').value = phone;
    document.getElementById('editPurchaseCount').value = purchaseCount;
    document.getElementById('editRemainingCount').value = remainingCount;

    // 打开模态框
    document.getElementById('editMemberModal').style.display = 'flex';
    //清空模态框

}

// 关闭编辑会员模态框
function closeEditMemberModal() {
    document.getElementById('editMemberModal').style.display = 'none';
}
//更新会员的剩余次数
function updateMember() {
    const name = document.getElementById('editName').value;
    const phone = document.getElementById('editPhone').value;
    const purchaseCount = document.getElementById('editPurchaseCount').value;
    const remainingCount = document.getElementById('editRemainingCount').value;
    var lable = 1
    // 简单的表单验证
    if (!name || !phone || !purchaseCount || !remainingCount) {
        alert('请填写所有字段');
        return;
    }
    // 发起 AJAX 请求将更新的数据发送到后端
    $.ajax({
        url: `/member-management/`,  // 假设后端提供了一个用于更新会员的 API
        method: 'PUT',
        contentType: 'application/json',
        headers: {'X-CSRFToken': getCSRFToken() },  // csrftoken 是你的 CSRF 令牌变量
        data: JSON.stringify({
            name: name,
            phone: phone,
            purchase_count: parseInt(purchaseCount),
            remaining_count: parseInt(remainingCount),
            lable:lable
        }),
        success: function (response) {
            alert('会员信息更新成功');
            closeEditMemberModal();
            location.reload();  // 刷新页面以查看更新后的数据
        },
        error: function (xhr, status, error) {
            alert('更新会员信息时出错，请稍后再试');
        }
    });
}
//新增会员的购买次数模态框
// 显示会员购买模态框
function showBuyMemberModal(memberId) {
    const row = document.querySelector(`#member-row-${memberId}`);
    const name = row.querySelector('.member-name').innerText;
    const phone = row.querySelector('.member-phone').innerText;
    const purchaseCount = row.querySelector('.member-purchase-count').innerText;
    // 将数据填充到模态框表单中
    document.getElementById('buyName').value = name;
    document.getElementById('buyPhone').value = phone;
    // 打开模态框
    document.getElementById('buyMemberModal').style.display = 'flex';
}
// 关闭会员购买模态框
function closeBuyMemberModal() {
    document.getElementById('buyMemberModal').style.display = 'none';
}
//会员购买次数
function buyMember()  {
    const name = document.getElementById('buyName').value;
    const phone = document.getElementById('buyPhone').value;
    const purchaseCount = document.getElementById('buyPurchaseCount').value;
    var lable = 2
    // 简单的表单验证
    if (!name || !phone || !purchaseCount) {
        alert('请填写所有字段');
        return;
    }
    // 发起 AJAX 请求将更新的数据发送到后端
    $.ajax({
        url: `/member-management/`,  // 假设后端提供了一个用于更新会员的 API
        method: 'PUT',
        contentType: 'application/json',
        headers: {'X-CSRFToken': getCSRFToken() },  // csrftoken 是你的 CSRF 令牌变量
        data: JSON.stringify({
            name: name,
            phone: phone,
            purchase_count: parseInt(purchaseCount),
            lable:lable
        }),
        success: function (response) {
            alert('会员信息更新成功');
            closeEditMemberModal();
            location.reload();  // 刷新页面以查看更新后的数据
        },
        error: function (xhr, status, error) {
            alert('更新会员信息时出错，请稍后再试');
        }
    });
}





















