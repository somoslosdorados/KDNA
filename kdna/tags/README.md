# tags.py API Documentation

This README file provides instructions on how to use the tags.py API to manage tags in your application.

## Installation

To use the tags.py API, you first need to import it:
> from kdna.tags import tags

## Usage

### Create a tag

To create a tag, you need to use the add_tags() function of the tags.py API. This function takes the following parameters:
- an instance of the fabric connection (obtained with the ssh.ssh_client module)
- the project name
- the tag name
- the name of the backup to tag

> tags.add_tags(ssh_client.connection, project_name, tag_name, backup_name)

### Delete a tag

To delete a tag, you need to use the delete_tags() function of the tags.py API. This function takes the following parameters:
- an instance of the fabric connection (obtained with the ssh.ssh_client module)
- the project name
- the tag name

> tags.delete_tags(ssh_client.connection, project_name, tag_name)

### Update a tag

To update a tag, you need to use the update_tags() function of the tags.py API. This function takes the following parameters:
- an instance of the fabric connection (obtained with the ssh.ssh_client module)
- the project name
- the tag name
- the new tag name

> tags.update_tags(ssh_client.connection, project_name, tag_name, new_tag_name)

### Get tags (Python dictionary)

To retrieve tags, you need to use the get_tag_conf() function of the tags.py API. This function takes the following parameters:
- an instance of the fabric connection (obtained with the ssh.ssh_client module)
- the project name

> tags.get_tag_conf(ssh_client.connection, project_name)
>> example return: {'tag1': 'backup1', 'tag2': 'backup2'}

### Generate a unique tag name (useful for cron)

To generate a unique tag name, you need to use the generate_tag_name() function of the tags.py API. This function takes the following parameters:
- an instance of the fabric connection (obtained with the ssh.ssh_client module)
- the project name
- a prefix

> tags.generate_tag_name(ssh_client.connection, project_name, prefix)

### Check if a tag exists

To check if a tag exists, you need to use the tag_exists() function of the tags.py API. This function takes the following parameters:
- an instance of the fabric connection (obtained with the ssh.ssh_client module)
- the project name
- the tag name

> tags.tag_exists(ssh_client.connection, project_name, tag_name)
>> returns True if the tag exists, False otherwise
