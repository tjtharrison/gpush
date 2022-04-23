#!/bin/bash

# Collect info
git_branch=$(git status | grep "On branch" | sed 's/On branch //g')
committed_files=$(git status | grep "Changes to be committed" | wc -l)

if [[ $committed_files -lt 1 ]]; then
    echo "No files committed"
    exit 1
fi

# Check PR readiness
PS3='Are you ready to PR this branch? '
choices=("yes" "no")
select choice in "${choices[@]}"; do
    case $choice in 
        "yes")
            commit_status="PR"
            break
            ;;
        "no")
            commit_status="WIP"
            break
            ;;
        *)
            echo "please select either: $choices"
    esac
done

if [[ $commit_status = "PR" ]]; then
# Check PR readiness
    PS3='How should we increment the semver? '
    semver_bump_choices=("major" "minor" "patch" "none")
    select semver_bump_choice in "${semver_bump_choices[@]}"; do
        case $semver_bump_choice in 
            "major")
                break
                ;;
            "minor")
                break
                ;;
            "patch")
                break
                ;;
            "none")
                break
                ;;
            *)
                echo "please select a valid option"
        esac
    done
fi

## Enter commit message
read -p 'Commit Message: ' commit_message

full_commit_message="$commit_status/$commit_message [$semver_bump_choice]"

## Confirmation
echo # Blank line
echo "Commit Message:"
echo $full_commit_message

echo "Okay, committing and pushing to $git_branch"
git commit -m "$full_commit_message"
git push origin $git_branch
