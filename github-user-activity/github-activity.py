import requests
import sys

if len(sys.argv) != 2:
    sys.exit("Invalid arguments. Usage: github-activity <username>")
else:
    username = sys.argv[1]

response = requests.get(f"https://api.github.com/users/{username}/events")

if response.ok:
    jsonify = response.json()

    for item in jsonify:
        payload = item["payload"]
        repo_name = item["repo"]["name"]

        match item["type"]:
            case "CommitCommentEvent":
                print(f"Comment on commit in {repo_name}")

            case "CreateEvent":
                print(f"Created {payload['ref_type']} in {repo_name}")

            case "DeleteEvent":
                print(f"Deleted {payload['ref_type']} in {repo_name}")

            case "ForkEvent":
                print(f"Forked {repo_name}")

            case "GollumEvent":
                print(f"Updated wiki in {repo_name}")

            case "IssueCommentEvent":
                print(f"Comment on issue {payload['issue']['html_url']}")

            case "IssuesEvent":
                print(f"{payload['action']} issue {payload['issue']['html_url']}")

            case "MemberEvent":
                print(f"Added member {payload['member'] in repo_name}")

            case "PublicEvent":
                print(f"{repo_name} made public")

            case "PullRequestEvent":
                print(
                    f"{payload['action']} pull request {payload['number']} in {repo_name}"
                )

            case "PullRequestReviewEvent":
                print(
                    f"{payload['action']} review for {payload['pull_request']['html_url']}"
                )

            case "PullRequestReviewCommentEvent":
                print(
                    f"{payload['action']} comment on {payload['pull_request']['html_url']} review"
                )

            case "PullRequestReviewThreadEvent":
                print(
                    f"{payload['action']} review thread on {payload['number']} in {repo_name}"
                )

            case "PushEvent":
                print(f"Pushed {payload['size']} commits to {repo_name}")

            case "ReleaseEvent":
                print(f"{payload['action']} release in {repo_name}")

            case "SponsorshipEvent":
                print(f"{payload['action']} sponsorship")

            case "WatchEvent":
                print(f"Starred {repo_name}")

else:
    print(response.status_code)
