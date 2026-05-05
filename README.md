# terraform-project
terraform analysis

## Jenkins Pipeline Setup

This repository includes a `Jenkinsfile` at the repo root for a declarative pipeline that:
- checks out the current branch from SCM
- runs Terraform init/plan/apply/destroy against `terraform-project/terraform`
- runs Trivy IaC and filesystem scans
- supports resource selection via build parameters

### Required Jenkins configuration

1. Create a new Jenkins job as a `Pipeline`.
2. Configure `Pipeline script from SCM`:
   - SCM: `Git`
   - Repository URL: `https://github.com/lochan-25/terraform-project.git`
   - Branch Specifier: `*/main`
   - Script Path: `Jenkinsfile`
3. Ensure the Jenkins agent has access to:
   - `git`
   - `terraform` (installed or configured as a Jenkins tool)
   - `trivy` for scanning
   - optional `sonar-scanner` if using Sonar analysis

### Terraform tool options

The pipeline attempts to use a Jenkins-managed Terraform tool named `terraform` first. If that tool is not configured, it falls back to the agent PATH.

#### Option A: Jenkins Terraform Tool
1. Go to `Manage Jenkins` → `Global Tool Configuration`.
2. Add a Terraform installation.
3. Use the exact tool name: `terraform`.

#### Option B: Terraform on PATH
1. Install Terraform on the Jenkins agent.
2. Make sure `terraform` or `terraform.exe` is available in the agent PATH.

### Pipeline parameters

When you run the job, Jenkins will show parameters for:
- `DRY_RUN` (`true`/`false`)
- `CREATE_EC2_INSTANCE`
- `CREATE_ELASTIC_IP`
- `CREATE_EBS_VOLUME`
- `CREATE_SNAPSHOT`

Use `DRY_RUN=true` for plan-only actions and `DRY_RUN=false` to apply/destroy selected resources.
