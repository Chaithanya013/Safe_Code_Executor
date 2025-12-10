# Docker Security Experiments – Report

## 1. Reading `/etc/passwd`

**Code tested:**

```python
with open("/etc/passwd") as f:
    print(f.read())
```

### Result

* This code **worked** inside the container.
* The API returned the contents of `/etc/passwd` from the **container’s filesystem**, not the host.

### What I learned

* Docker containers include system files like `/etc/passwd`.
* These files are readable unless explicitly restricted.
* Docker **does not** block reading files that already exist inside the container.

---

## 2. Writing to `/tmp/test.txt` (before `--read-only`)

**Code tested:**

```python
with open("/tmp/test.txt", "w") as f:
    f.write("hacked!")
with open("/tmp/test.txt") as f:
    print(f.read())
```

### Result (before applying `--read-only`)

* The file write **succeeded**.
* The API returned:

```
hacked!
```

* The file existed only inside the temporary container and disappeared afterward (`--rm` removes the container).

### What I learned

* By default, containers have a **writable** filesystem.
* Code inside a container can create, modify, or delete files within the container.
* These writes do **not** affect the host unless a mounted volume is used.

---

## 3. Writing to `/tmp/test.txt` after adding `--read-only`

**Docker command update:**

```
--read-only
```

### Result (after applying `--read-only`)

* Writing to `/tmp/test.txt` **failed**.
* The API returned an error such as:

```
OSError: [Errno 30] Read-only file system: '/tmp/test.txt'
```

### What I learned

* `--read-only` makes the container’s root filesystem **read-only**.
* User code can no longer write to locations like `/tmp`.
* This prevents malicious code from modifying the container’s filesystem.

---

## Overall Learnings About Docker Security

* Containers isolate processes but **are not magically secure**.
* Code inside a container:

  * **Can read** files that exist inside the container
  * **Can write** to the filesystem **unless** you use `--read-only`
  * **Cannot use the network** if `--network none` is set
  * **Cannot exceed memory limits** if `--memory` is set
* Docker helps sandbox untrusted code, but full security requires multiple layers:

  * Resource limits
  * No network access
  * Read-only filesystems
  * Non-root users (future steps)
  * Optional seccomp/AppArmor for real deployments
