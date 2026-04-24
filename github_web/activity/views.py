from django.shortcuts import render
import urllib.request
import urllib.error
import json


# Fetch user activity
def fetch_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    request = urllib.request.Request(url)
    request.add_header("User-Agent", "django-app")

    try:
        response = urllib.request.urlopen(request)
        data = response.read()
        return json.loads(data)

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        return []

    except urllib.error.URLError:
        return []


# Fetch user profile
def fetch_profile(username):
    url = f"https://api.github.com/users/{username}"
    request = urllib.request.Request(url)
    request.add_header("User-Agent", "django-app")

    try:
        response = urllib.request.urlopen(request)
        data = response.read()
        return json.loads(data)

    except:
        return None


# Main view
def home(request):
    context = {}

    if request.method == "POST":
        username = request.POST.get("username").strip()

        events = fetch_activity(username)
        profile = fetch_profile(username)

        # Handle user not found
        if events is None:
            context["error"] = "❌ User not found"
            return render(request, "activity/index.html", context)

        formatted_events = []

        for event in events[:10]:
            event_type = event.get("type")
            repo = event.get("repo", {}).get("name")

            if event_type == "PushEvent":
                icon = "📌"
                text = f"Pushed commits to {repo}"

            elif event_type == "PullRequestEvent":
                icon = "🔀"
                text = f"Opened a pull request in {repo}"

            elif event_type == "IssuesEvent":
                icon = "🐛"
                text = f"Worked on issues in {repo}"

            elif event_type == "IssueCommentEvent":
                icon = "💬"
                text = f"Commented on an issue in {repo}"

            elif event_type == "CreateEvent":
                icon = "🆕"
                text = f"Created something in {repo}"

            elif event_type == "DeleteEvent":
                icon = "🗑️"
                text = f"Deleted something in {repo}"

            elif event_type == "WatchEvent":
                icon = "⭐"
                text = f"Starred {repo}"

            elif event_type == "ForkEvent":
                icon = "🍴"
                text = f"Forked {repo}"

            else:
                icon = "🔹"
                text = f"{event_type} in {repo}"

            formatted_events.append({
                "icon": icon,
                "text": text
            })

        context = {
            "username": username,
            "events": formatted_events,
            "profile": profile
        }

    return render(request, "activity/index.html", context)