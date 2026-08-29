from test_data.routes import ROUTES
from test_data.todos import TODO_DATA


def test_add_and_complete_todos(todo_page):
    data = TODO_DATA["add_and_complete"]
    first_todo = data["first_todo"]
    second_todo = data["second_todo"]

    todo_page.open_fresh_todomvc()

    todo_page.add_todo(first_todo)
    todo_page.add_todo(second_todo)

    todo_page.assert_total_items(2)
    todo_page.assert_items_left(2)
    todo_page.assert_toggle_checked(first_todo, checked=False)
    todo_page.assert_toggle_checked(second_todo, checked=False)

    todo_page.toggle_todo(first_todo)

    todo_page.assert_item_completed(first_todo)
    todo_page.assert_toggle_checked(first_todo)
    todo_page.assert_items_left(1)
    todo_page.assert_item_not_completed(second_todo)
    todo_page.assert_toggle_checked(second_todo, checked=False)


def test_filter_behaviour_is_correct(todo_page):
    data = TODO_DATA["filter_scenario"]
    task_a = data["task_a"]
    task_b = data["task_b"]
    task_c = data["task_c"]

    todo_page.open_fresh_todomvc()

    todo_page.add_todo(task_a)
    todo_page.add_todo(task_b)
    todo_page.add_todo(task_c)

    todo_page.assert_total_items(3)
    todo_page.assert_items_left(3)

    todo_page.toggle_todo(task_b)

    todo_page.assert_item_completed(task_b)
    todo_page.assert_items_left(2)

    todo_page.select_filter("Active")
    todo_page.assert_selected_filter("Active", ROUTES["active"])
    todo_page.assert_total_items(2)
    todo_page.visible_todo_item(task_a)
    todo_page.visible_todo_item(task_c)
    todo_page.assert_item_not_present(task_b)

    todo_page.select_filter("Completed")
    todo_page.assert_selected_filter("Completed", ROUTES["completed"])
    todo_page.assert_total_items(1)
    todo_page.visible_todo_item(task_b)
    todo_page.assert_item_not_present(task_a)
    todo_page.assert_item_not_present(task_c)

    todo_page.select_filter("All")
    todo_page.assert_selected_filter("All", ROUTES["all"])
    todo_page.assert_total_items(3)
    todo_page.assert_toggle_checked(task_a, checked=False)
    todo_page.assert_toggle_checked(task_b)
    todo_page.assert_toggle_checked(task_c, checked=False)
