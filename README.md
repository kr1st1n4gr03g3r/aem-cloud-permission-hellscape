# 🔥 AEM Cloud Permission Hellscape 🔥
Have you ever spent hours and days banging your head against your desk at AEM Cloud permissions? This is an application to get you out of permissions hell in AEMaacS that helps visualize nested permissions.

### Installation Instructions:

1. Create a package in CRXDE with the contents of your `/home` directory, and download the ZIP.
2. Unzip the contents. Cut / copy the folder `jcr_root/home`, and paste it into `home-package-dump`.
3. Ensure that the folder structure is as follows, and nothing else in the`home-package-dump` folder.
```
home-package-dump/home/users
home-package-dump/home/groups
home-package-dump/home/_rep_policy.xml
```

In the root of