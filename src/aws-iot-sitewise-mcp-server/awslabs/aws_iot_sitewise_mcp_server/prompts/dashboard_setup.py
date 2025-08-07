"""AWS IoT SiteWise Dashboard Setup Helper Prompt."""

from mcp.server.fastmcp.prompts import Prompt


def dashboard_setup_helper(use_case: str, assets: str) -> str:
    """Generate a comprehensive guide for setting up monitoring dashboards in AWS IoT SiteWise.

    This prompt helps design and implement monitoring solutions including portal creation,
    project organization, dashboard design, and access control.

    Args:
        use_case: Description of the monitoring use case
        assets: Description of assets to monitor

    Returns:
        Comprehensive dashboard setup strategy guide
    """
    return f"""
You are an AWS IoT SiteWise Monitor expert helping to set up comprehensive monitoring dashboards.

**Use Case**: {use_case}
**Assets to Monitor**: {assets}

Please provide a complete dashboard setup strategy following these steps:

1. **Portal Planning and Setup**:
   - Design portal structure for the use case
   - Use create_portal to set up the main monitoring portal
   - Configure portal settings including:
     - Authentication mode (IAM/SSO)
     - Contact email and notifications
     - Logo and branding
     - Alarm configuration

2. **Access Control Strategy**:
   - Plan user roles and permissions (ADMINISTRATOR, VIEWER)
   - Use create_access_policy to set up access policies
   - Configure policies for different user groups:
     - Operations team (full access)
     - Management (read-only dashboards)
     - Maintenance (specific asset access)
   - Set up IAM roles and policies

3. **Project Organization**:
   - Design project structure to organize dashboards logically
   - Use create_project to create projects for:
     - Different production lines/areas
     - Asset types or systems
     - Operational vs. analytical views
   - Plan project hierarchy and asset associations

4. **Asset Association and Management**:
   - Use list_assets to identify available assets
   - Associate relevant assets with projects
   - Organize assets by:
     - Physical location
     - System type
     - Criticality level
     - Maintenance schedule

5. **Dashboard Design Strategy**:
   - Plan dashboard layouts for different audiences:
     - Executive summary dashboards
     - Operational monitoring dashboards
     - Maintenance and diagnostic dashboards
     - Historical analysis dashboards

6. **Dashboard Implementation**:
   - Use create_dashboard to create dashboards with:
     - Real-time asset property displays
     - Historical trend charts
     - Alarm status indicators
     - KPI summaries
     - Asset hierarchy navigation

7. **Widget Configuration**:
   - Configure different widget types:
     - Line charts for trends
     - Bar charts for comparisons
     - Status indicators for alarms
     - Tables for asset properties
     - Maps for asset locations
   - Set up proper time ranges and aggregations

8. **Data Visualization Best Practices**:
   - Use appropriate chart types for different data
   - Configure meaningful color schemes
   - Set up proper scaling and units
   - Implement drill-down capabilities
   - Add contextual information and annotations

9. **Alerting and Notifications**:
   - Configure alarm thresholds and conditions
   - Set up notification channels
   - Design alarm escalation procedures
   - Implement alarm acknowledgment workflows

10. **Performance and Optimization**:
    - Optimize dashboard loading times
    - Configure appropriate data refresh rates
    - Use aggregated data for historical views
    - Implement caching strategies

11. **Mobile and Responsive Design**:
    - Ensure dashboards work on mobile devices
    - Design for different screen sizes
    - Consider offline capabilities

12. **Testing and Validation**:
    - Test dashboards with real data
    - Validate alarm conditions
    - Check performance under load
    - Gather user feedback and iterate

**Deliverables**:
- Portal and project setup plan
- Access control matrix
- Dashboard wireframes and specifications
- JSON dashboard definitions
- User training materials
- Maintenance procedures

**Sample Dashboard Types to Create**:

1. **Executive Dashboard**:
   - Overall equipment effectiveness (OEE)
   - Production metrics
   - Energy consumption
   - Alarm summary

2. **Operations Dashboard**:
   - Real-time asset status
   - Current production rates
   - Active alarms
   - Shift performance

3. **Maintenance Dashboard**:
   - Asset health indicators
   - Predictive maintenance alerts
   - Maintenance schedules
   - Historical failure analysis

4. **Energy Management Dashboard**:
   - Power consumption trends
   - Energy efficiency metrics
   - Cost analysis
   - Sustainability indicators

**Implementation Steps**:
1. Create portal with proper configuration
2. Set up access policies for different user roles
3. Create projects for logical organization
4. Associate assets with appropriate projects
5. Design and create dashboards for each use case
6. Configure widgets and visualizations
7. Set up alarms and notifications
8. Test and validate with stakeholders
9. Deploy and train users
10. Monitor usage and optimize

Please provide specific JSON configurations, best practices, and troubleshooting guidance.
Include sample dashboard definitions and widget configurations for the specified use case.
"""


# Create the prompt using from_function
dashboard_setup_helper_prompt = Prompt.from_function(
    dashboard_setup_helper,
    name='dashboard_setup_helper',
    description='Generate a comprehensive guide for setting up monitoring dashboards in AWS IoT SiteWise',
)
