# Level 2

http://level2-c8b217a33fcf1f839f6f1f73a00a9ae7.flaws.cloud/

<img width="825" height="776" alt="image" src="https://github.com/user-attachments/assets/f93fa40c-2fc5-44d1-9b85-855198fcd2e6" />

<img width="747" height="322" alt="image" src="https://github.com/user-attachments/assets/c1b68c0e-c164-41dc-89ec-83978f563768" />

Attempting to enumerate the bucket anonymously results in an `AccessDenied` error. This indicates that the bucket does not permit the `ListBucket` action for unauthenticated users. However, denying bucket listing does not guarantee that objects themselves are private, as individual files may still be accessible if their names are known. Stated needing an aws account for this.

```
aws s3 ls s3://level2-c8b217a33fcf1f839f6f1f73a00a9ae7.flaws.cloud --no-sign-request

An error occurred (AccessDenied) when calling the ListObjectsV2 operation: Access Denied
```
