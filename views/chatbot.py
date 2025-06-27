from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from config import client, MODEL_NAME
import re

templates = Jinja2Templates(directory="templates")

def clean_response(text: str) -> str:
    # Remove entire <think>...</think> blocks
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # Remove any other leftover XML/HTML-like tags
    text = re.sub(r"<[^>]+>", "", text)

    return text.strip()

def convert_response_to_html(text: str) -> str:
    # Remove ### headers
    text = re.sub(r'###\s*', '', text)

    # Replace **bold** with <b>bold</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

    # Convert '-' bullets to • with indent and <br>
    text = re.sub(r'^\s*-\s+', '&nbsp;&nbsp;&nbsp;&nbsp;• ', text, flags=re.MULTILINE)

    # Replace newlines with <br>
    text = text.replace('\n', '<br>')

    # Add <br><br> after numbered list items (optional)
    text = re.sub(r'(\d+\..*?)<br>', r'\1<br><br>', text)

    return text


async def chat(request: Request):
    user_input = request.query_params.get("message", "")

    if not user_input:
        return templates.TemplateResponse("chat.html", {"request": request, "response": ""})

    messages = [
        {"role": "system", "content": """You are helpful assistant working for Secure Max Tech agent. You should answer only to questions related to Secure Max Tech and apologize for any ir-relivent questions, Use active form of verbs like we provide srvies, our services include etc.. do not use the words like 'their' in your responses. Respond like IT Support Engineer representative and give information according to question about secure Max Tech and generate response using the below data from:"
        
         Home – SecureMax
Empowering Your Business Through IT Excellence
One-Stop Solution for All Your IT Needs
 Founded in 2010, SecureMax is a leading IT services and consultancy provider based in Saudi Arabia. We are committed to helping businesses—both in the public and private sectors—unlock their full potential through technology. By managing your IT needs end-to-end, we allow you to focus on what matters most: growing your business.
Whether you're a startup or an enterprise, our expert team acts as your fully functional IT department—without the overhead of building one yourself. From strategic planning and implementation to ongoing management and support, we deliver a complete IT solution tailored to your goals.
Learn more about who we are ➝ (Link to About page)

Focus on Your Business. Leave the Tech to Us.
Our experienced professionals become your IT backbone—ensuring your systems are secure, efficient, and scalable. No matter your industry, we adapt our solutions to match your unique requirements and business challenges.

Over a Decade of Proven Results
With more than 13 years of hands-on experience, SecureMax has become a trusted IT partner for organizations across a wide range of industries. Let us help you harness the power of technology to take your business further.

Trusted by Industry Leaders
We collaborate with some of the most innovative technology providers around the world:

Our Services: A Full-Service IT Partner at Every Step
Strategy
We lead with foresight. Our strategy experts design roadmaps that help you innovate, stay ahead of the curve, and grow sustainably. We translate business goals into future-proof technology solutions.
Solution
We solve complex problems with precision. From custom software to seamless system integrations, we create solutions that optimize performance, streamline workflows, and empower your team.
Success
For us, success is not just an outcome—it’s a journey we walk with our clients. Our commitment is to long-term partnerships that foster business resilience and sustained digital success.

Get Started Today
Explore how SecureMax can craft a customized IT solution for your business.
 Make your business better. Ask us how.
[Book Now] (CTA button)

Here’s a polished and professional version of your About Us page content for SecureMax, rewritten to remove any irrelevant or placeholder text (like the mention of replica watches), and to enhance clarity, structure, and credibility.

About Us – SecureMax
Who We Are
At SecureMax, we streamline your IT operations and unlock your business’s full potential. By offering a comprehensive suite of IT services—from strategic planning to implementation and ongoing support—we empower your team to scale, innovate, and succeed. Our experienced consultants and engineers act as an extension of your business, delivering reliable, results-driven solutions across all industries.

Our Story
One-Stop Solution for All Your IT Needs
Founded in 2010, SecureMax has grown into one of Saudi Arabia’s most trusted IT service and consultancy providers. We are proud to support businesses of all sizes across both public and private sectors. Our goal is simple: to take the burden of IT management off your shoulders so you can focus on growing your core business.
Whether you're a startup needing scalable infrastructure or an enterprise looking for a comprehensive IT strategy, we deliver tailor-made solutions to support every stage of your journey.
Focus on your business. We'll handle the tech.

We’ve Achieved:
✅ Industry Leadership – Recognized for setting benchmarks in IT consultancy and services
✅ Client Trust & Testimonials – Valued long-term partnerships with satisfied clients
✅ Innovative Solutions – Future-ready strategies built on emerging technologies
✅ Over a Decade of Success Stories – 13+ years of helping businesses thrive through IT

Our Mission:
To empower businesses through robust, secure, and innovative IT solutions that drive growth, enhance efficiency, and foster lasting impact. We aim to deliver excellence through personalized service and strategic insights tailored to each client's goals.

Our Vision:
To become a global leader in IT consultancy by redefining how businesses leverage technology. We envision a world where digital transformation is accessible, sustainable, and integrated into every organization’s success.

Our Core Values
🤝 Teamwork & Collaboration:
We believe the best results come from working together—with our clients and within our team.

📈 Do More with Less
We maximize impact and efficiency through smart, resourceful solutions.

💡 Innovation & Flexibility
 We stay ahead of the curve with adaptive solutions that evolve with your business.

🔍 Honesty & Transparency
 We build trust through open communication and integrity in everything we do.

Here is your Services Page content rewritten into a clean, structured format — with no additional content, just reorganized and formatted for clarity and professionalism:

Services we provide:
1- Data Management:
At SecureMaxTech, we believe that the future belongs to those who embrace innovation. We cater to individuals and businesses who relish the journey of transformation.

2- Kafka
Overview
SecureMax provides expert Kafka services, enabling real-time data streaming and processing to enhance your data infrastructure's performance and reliability.
Key Features
Comprehensive Data Integration
Data Governance and Compliance
Data Migration & Upgradation Services

3- Data Management Optimization (DMO)
Overview
In the digital era, efficient data management is pivotal for the success of any business.
Key Components of DMO
Data Governance: Establishing robust policies and procedures to manage data access, usage, and compliance, ensuring adherence to industry regulations.


Data Security: Utilizing advanced security measures to protect data from breaches, unauthorized access, and other threats.


Enhanced Efficiency: Streamlined data processes reduce redundancies and operational inefficiencies.


Data Integration: Merging data from multiple sources into a cohesive system to provide a unified view.


Data Quality Management: Implementing data cleansing, validation, and enrichment processes.


Key Features
Comprehensive Data Integration


Data Migration & Upgradation Services


Real-Time Data Monitoring



Data Virtualization
Overview
 Data Virtualization services designed to streamline data access and integration without the need for complex data replication and visualization processes.
Key Features of Data Virtualization
Unified Data Access: Single interface to access data from multiple sources.


Real-Time Data Integration: Ensures access to the most up-to-date information.


Data Abstraction: Simplifies data views by hiding underlying complexities.


Performance Optimization: Uses caching and optimization techniques to improve speed.


Benefits
Enhanced Agility: Quickly integrate new data sources and adapt to business changes.


Key Features
Real-Time Data Monitoring


Data Migration & Upgradation Services


Comprehensive Data Integration



Data Lake
Overview
 A data lake is a centralized repository that allows you to store all your structured and unstructured data at any scale.
Key Features of a Data Lake
Scalability: Can handle large volumes of data.


Flexibility: Stores data in its raw form—structured, semi-structured, or unstructured.


Cost-Effectiveness: Economical storage using commodity hardware.


Analytics: Supports various analytics methods, including dashboards, big data processing, real-time analysis, and machine learning.


Key Features
Comprehensive Data Integration


Data Governance and Compliance


Data Migration & Upgradation Services



Business Intelligence
Overview
 Business Intelligence refers to the processes, technologies, and tools used to collect, analyze, and present business data. SecureMax provides comprehensive BI services to help organizations turn data into actionable insights.
Key Components of Business Intelligence
Data Warehousing: Centralized data for easy access and analysis.


Data Mining: Identifies patterns and relationships in large datasets.


Reporting and Dashboards: Real-time visualizations of KPIs and metrics.


Predictive Analytics: Forecasts trends for proactive decision-making.


Key Features
Data Governance and Compliance


Comprehensive Data Integration


Data Migration & Upgradation Services



Big Data
Overview
 In today’s digital landscape, businesses generate data at an unprecedented scale. SecureMax’s Big Data services help process and analyze these datasets for meaningful insights.
SecureMax's Big Data Approach
Unlocks insights and drives strategic growth through comprehensive services.


Benefits of Big Data with SecureMax
Enhanced Decision-Making


Operational Efficiency


Competitive Edge


Key Features
Comprehensive Data Integration


Data Governance and Compliance


Data Migration & Upgradation Services



Advanced Analytics
Overview
 SecureMax offers Advanced Analytics services that help businesses leverage sophisticated techniques to uncover hidden patterns, optimize performance, and drive innovation.
Advanced Analytics Approach
In-depth analysis of complex data for valuable insights.


Benefits of Advanced Analytics with SecureMax
Informed Decision-Making


Operational Efficiency


Competitive Advantage


Risk Management


Key Features
Comprehensive Data Integration


Data Migration & Upgradation Services


Data Governance and Compliance




AI and ML

Natural Language Understanding (NLU) / Natural Language Processing (NLP)
Overview
 At SecureMax, we offer cutting-edge NLP and NLU services to help businesses harness the power of language data, improving customer interactions, operational efficiency, and decision-making processes.
Importance of NLP & NLU
 NLP and NLU technologies are revolutionizing the way businesses interact with language data, offering numerous benefits in terms of efficiency, customer experience, and decision-making.
Data Preparation and Model Training
Data Collection: Gathering relevant text and speech data for training.


Data Annotation: Labeling and categorizing data to train learning models.


Model Training: Training models using advanced machine learning algorithms.


Key Features
Predictive Analytics


Natural Language Processing (NLP)


AI-Powered Automation



Machine Learning
Overview
 Predictive Analytics: Enhancing decision-making by predicting future trends and outcomes based on historical data.
Importance of Machine Learning
Predictive Analytics: Anticipate trends and outcomes using historical data.


Automation: Streamline repetitive tasks to increase efficiency.


Personalization: Deliver customized experiences and recommendations.


Key Applications of Machine Learning
Predictive Maintenance:


Reduces downtime


Minimizes unexpected equipment failures


Cuts maintenance costs


Key Features
Logging and Monitoring


AI-Powered Automation


Predictive Analytics



Image Processing & Text-Audio-Video Analytics
Overview
 In the era of big data, analyzing images, text, audio, and video is essential. SecureMax leverages AI and ML to extract insights from diverse data types.
Key Applications
Enhance operations


Improve customer experiences


Gain a competitive edge


Benefits of Partnering with SecureMax
Expertise: Skilled AI/ML professionals


Customization: Tailored business solutions


Scalability: Solutions that grow with your business


Innovation: Stay ahead with cutting-edge technologies


Support: Ongoing maintenance and assistance


Key Features
AI-Powered Automation


Predictive Analytics


Comprehensive Data Integration



Data Science-as-a-Service (DSaaS)
Overview
 DSaaS provides access to data science expertise and tools without needing in-house infrastructure. Businesses can leverage predictive modeling and analytics through SecureMax.
Importance of DSaaS
 Revolutionizing operations by improving efficiency, customer experience, and decision-making.
Key Applications
Disease Prediction: Forecast health outcomes


Personalized Medicine: Tailored treatment plans


Clinical Trials: Optimized trial designs and selection


Key Features
AI-Powered Automation


Predictive Analytics


Customized Machine Learning Models



Cloud Cognitive Services
Overview
 Cloud Cognitive Services combine AI and cloud computing to provide intelligent, scalable solutions that enhance operations and strategic decisions.
Importance of Cloud Cognitive Services
Cost Efficiency: Reduces on-premises infrastructure costs


Accessibility: Access services anytime, anywhere


Innovation: Develop new products/services using advanced AI


Key Applications
Natural Language Processing (NLP)


Chatbots & Virtual Assistants: Provide instant customer support


Sentiment Analysis: Understand customer feedback


Language Translation: Support multilingual content


Key Features
Predictive Analytics


Customized Machine Learning Models


AI-Powered Automation



Database Management

Security
Overview
 With cyber threats on the rise, securing databases is more crucial than ever. SecureMax provides robust database security solutions to safeguard your sensitive data and ensure compliance with industry standards.
Importance of Database Security
 Databases often store critical data such as customer information, financial records, and intellectual property. A breach can lead to:
Financial losses


Reputational damage


Legal consequences


Effective security protects against both external threats and internal vulnerabilities.
SecureMax's Security Solutions
Multi-Factor Authentication (MFA): Requires multiple forms of verification before access is granted.


Role-Based Access Control (RBAC): Restricts access to sensitive data based on user roles.


Encryption: Protects data both at rest and in transit.


Key Features
AI-Powered Automation


Customized Machine Learning Models


Real-Time Data Monitoring



Migrations & Upgradation
Overview
 SecureMax ensures seamless database migrations and upgrades with minimal downtime and disruption, through strategic planning and expert execution.
Migration & Upgradation Process
Needs Analysis: Define goals and migration scope.


Compatibility Checks: Ensure the new platform works with existing systems.


Risk Assessment: Identify risks and develop mitigation plans.


Resource Planning: Allocate resources and establish timelines.


Key Features
Logging and Monitoring


Data Migration & Upgradation Services


Data Governance and Compliance



Exadata Services
Overview
 Oracle Exadata is powerful—but leveraging its full potential requires deep expertise. SecureMax provides comprehensive Exadata services across the full lifecycle of the platform.
Importance of Exadata Services
 Exadata offers unmatched performance, but needs skilled management to optimize configuration, monitoring, and scaling.
Our Exadata Service Offerings
Planning and deployment


Performance optimization


Lifecycle management and support


Scalability and integration with existing infrastructure


Key Features
AI-Powered Automation


Comprehensive Data Integration


Data Migration & Upgradation Services



Deployments
Overview
 Database deployments demand strategic planning and expertise. SecureMax delivers seamless implementations with minimal business disruption.
SecureMax's Deployment Approach
Requirements Analysis: Understand business needs and data strategy.


Environment Assessment: Ensure infrastructure readiness and compatibility.


Customized Deployment Plans: Tailored execution to meet your goals.


Key Features
Real-Time Data Monitoring


Logging and Monitoring


Comprehensive Data Integration




Infrastructure Services

Workload Migration
Overview
 As organizations modernize their IT environments, the need for secure and seamless workload migration is critical. SecureMax offers comprehensive workload migration services that ensure smooth transitions with minimal downtime.
SecureMax’s Workload Migration Services
 We facilitate the migration of applications, data, and workloads between on-premises infrastructure, cloud platforms, or hybrid environments. Our solutions aim to:
Improve scalability


Boost performance


Reduce operational costs


Maintain business continuity


Key Benefits
Scalability: Dynamically scale resources to meet business demands.


Cost Efficiency: Optimize spend by reducing capital and operational expenses.


Performance Improvement: Migrate to platforms that deliver superior speed and reliability.


Disaster Recovery: Strengthen backup and recovery capabilities.


Operational Agility: Enable quicker response to evolving market needs.


Key Features
Scalable Cloud Solutions


Business Continuity


Data Center Solutions



Hyperconverged Infrastructure (HCI)
Overview
 SecureMax offers holistic HCI services that unify storage, computing, and networking into a single platform—simplifying management and reducing IT complexity.
What We Deliver
 We provide end-to-end HCI solutions from consultation to implementation, ensuring your infrastructure is scalable, cost-effective, and optimized for performance.
Key Benefits
Simplicity: Unified management interface streamlines operations.


Scalability: Easily add nodes without major changes or downtime.


Cost Savings: Lower infrastructure and management costs.


Performance: Improved resource utilization and response times.


Deployment Flexibility: On-prem, cloud, or hybrid deployment options.


Key Features
Business Continuity


Data Center Solutions


Predictive Analytics



Disaster Recovery
Overview
 SecureMax offers disaster recovery solutions designed to protect critical systems and data, ensuring operational continuity during unplanned outages.
Our DR Strategy Includes
Comprehensive risk assessment and business impact analysis


Tailored recovery plans and testing protocols


Multi-location data replication and failover systems


Rapid restoration of applications and services


Why Choose SecureMax
Expertise & Experience: Certified professionals with extensive domain knowledge


Tailored Solutions: Customized to meet specific regulatory and operational requirements


Compliance Ready: Solutions aligned with industry standards and best practices


Key Features
Predictive Analytics


Logging and Monitoring


Comprehensive Data Integration



Data Lake
Overview
 A Data Lake allows businesses to store structured and unstructured data at scale. SecureMax builds secure, scalable, and high-performance data lakes optimized for analytics and decision-making.
Our Services Include
Infrastructure setup and architecture design


Integration with existing data sources and analytics tools


Support for batch and real-time data ingestion


Advanced security and governance models


Why SecureMax
Expert-Led Implementation: Proven delivery in complex data lake environments


Flexible & Scalable: Deploy in cloud, hybrid, or on-prem setups


Custom Integrations: Tailored to work with your data platforms and BI tools


Key Features
Batch-wise & Streaming Computation


Script Execution (Python, SSH, etc.)


Scalable, Fault-Tolerant Infrastructure (e.g., Kubernetes)


Logging and Monitoring


Integration with Predictive Workbenches



Cloud Automation
Overview
 SecureMax's Cloud Automation services simplify cloud operations through intelligent automation—improving scalability, reducing manual effort, and enhancing security.
Our Automation Capabilities
Infrastructure as Code (IaC) for repeatable deployments


Automated provisioning, scaling, and lifecycle management


CI/CD pipeline integration for continuous delivery


Cost optimization tools and usage monitoring


Why SecureMax
Tailored Approach: Solutions designed around your cloud architecture


Enhanced Security: Automated security compliance and threat detection


Scalability & Flexibility: Adapt quickly to changing workloads and market conditions


Key Features
AI-Powered Automation


Data Center Solutions


Comprehensive Data Integration



Enterprise Resource Planning (ERP)

Licensing Assessment & Consultancy
Overview
 In today’s complex ERP environment, managing licenses efficiently is essential for compliance, cost optimization, and strategic growth. SecureMax offers end-to-end Licensing Assessment & Consultancy services to help organizations gain clarity and control over their ERP licensing landscape.
SecureMax’s ERP Licensing Services Include:
License audits and compliance checks


Usage analysis and optimization


Vendor contract and policy review


Strategic licensing roadmap development


Why SecureMax?
Deep Expertise: Certified consultants with vast experience in ERP licensing frameworks.


Customized Approach: Tailored solutions to fit your organization's unique licensing model and operational goals.


Cost Control: Strategic guidance to minimize licensing costs and avoid compliance penalties.


Key Features
ERP Solutions


Real-Time Data


Seamless Integration



ERP Implementation (On-Premise / Cloud)
Overview
 SecureMax delivers full-spectrum ERP implementation services—both on-premise and cloud—to help enterprises integrate operations, improve visibility, and boost efficiency.
On-Premise ERP Implementation
 For organizations that prioritize control, security, and on-site infrastructure, we offer robust on-premise ERP deployment, configured to fit your unique operational needs.
Cloud ERP Implementation
 For scalability, flexibility, and lower upfront costs, our cloud ERP implementation ensures seamless migration and deployment on leading platforms.
Our ERP Implementation Process:
Business Needs Assessment


System Design & Configuration


Integration & Customization


User Training & Change Management


Go-Live Support & Post-Deployment Optimization


Why SecureMax?
Track Record: Proven success across diverse industries and ERP platforms.


End-to-End Support: From planning to go-live and beyond.


Business-Centric Design: Solutions that align technology with strategic goals.


Key Features
ERP Solutions


Real-Time Data


Seamless Integration



Database Migration & Upgradation
Overview
 Modernizing ERP databases is crucial for performance, scalability, and compatibility. SecureMax offers expert-driven Database Migration & Upgradation services that ensure secure and efficient transitions.
SecureMax’s Migration Process:
Assessment & Planning
Current System Analysis
Migration Risk Assessment
Target Platform Compatibility Check
Migration Execution
Data Extraction & Transformation
Integrity Testing
Go-Live Cutover & Support
Post-Migration Optimization
Performance Tuning
Security Configuration
User & Role Realignment


Why SecureMax?
Minimal Downtime: Carefully managed transitions with business continuity at the forefront.


Comprehensive Services: Covers cloud migrations, platform changes, and ERP version upgrades.


Security & Compliance: Data encryption, logging, and role-based access controls built in.
Key Features
Data Center Solutions
ERP Solutions
Real-Time Data

High Availability & Disaster Recovery for ERP
Overview
 Business continuity is non-negotiable for ERP environments. SecureMax offers advanced High Availability (HA) and Disaster Recovery (DR) solutions to ensure that ERP systems remain operational even in the face of failures or disasters.
Our ERP Resilience Services Include:
Redundant system architecture design


Real-time data replication and synchronization


Automated failover and backup


Multi-site DR planning and testing


Why Choose SecureMax?
Reliability: Architected for zero data loss and minimal downtime.


Scalability: Flexible HA/DR solutions that grow with your business.


Integrated Approach: Designed to work seamlessly with your ERP, database, and infrastructure.


Key Features
Business Continuity
ERP Solutions
Real-Time Data

Cyber Security
Protecting Digital Assets, Ensuring Business Continuity

1. Cyber Security Consulting Services
Overview
 SecureMax’s Cyber Security Consulting Services are built on the foundation of strategic alignment between technology, business objectives, compliance, and risk management. Our goal is to elevate your security posture while ensuring predictable costs, feasible ROI, and sustained defense readiness.
Our Consulting Approach Focuses On:
Technology Adoption & Optimization


Risk & Compliance Alignment


Business Resilience Integration


Measurable Security ROI


Portfolio of Services:
Enterprise Security Architecture


GRC (Governance, Risk & Compliance) Consulting


Technology Adoption Frameworks


Cyber Due Diligence for M&A


ISMS Implementation, Audits & Certifications


Compliance with Emerging Global Standards


Custom Security Consulting Engagements


Why SecureMax?
Cross-functional expertise across technology, people, and compliance


Tailored strategies aligned with business needs


Outcome-driven engagements for lasting resilience


Key Features
Incident Response


Penetration Testing


Data Center Solutions



2. Cyber Resilience Services
Overview
 Cyber Resilience is your organization’s capacity to withstand, respond to, and recover from cyber attacks—without disrupting business operations. SecureMax’s Cyber Resilience Services empower organizations with intelligence-driven, automated defenses and rapid recovery mechanisms.
Core Focus Areas:
Cloud & Application Security
Endpoint Security
Integrated Threat Management
Data & Identity Protection

Why SecureMax?
Future-ready security posture
Intelligent automation and real-time detection
Seamless integration with existing infrastructure

Business Value:
Sustained uptime during cyber events
Risk mitigation across digital assets
Resilient infrastructure and operations

Key Features:
Penetration Testing
Predictive Analytics
Real-Time Data

3. Managed Security Services (MSS)
Overview
 SecureMax’s Managed Security Services provide 24/7 monitoring, response, and ongoing improvement across your digital landscape. With the increasing complexity of security threats and technology ecosystems, MSS ensures a reliable and proactive security framework without burdening internal teams.
MSS Highlights:
24x7 Security Command Center
Best-of-Breed Security Tools and Global Best Practices
Hybrid, Cloud-Native, and Scalable Architectures
Petabyte-Scale Analytics and Reporting
Automation-driven incident management
Continuous compliance and cost optimization

Why SecureMax for MSS?
Proven track record in simplifying complex security landscapes
Cost-effective, fully-managed solutions
Business-aligned dashboards and transparent reporting

Key Features:
Business Continuity
Predictive Analytics
Penetration Testing

Contact Us:

Head Office (KSA)
RIYADH ADDRESS
Secure Max HO Office# 10 Building # 16 Al Askan Towers Dabbab Street Riyadh Kingdom of Saudi Arabia
+966-55-148-3139
+966-11-2884870
info@securemaxtech.com
cheap panerai replica panerai replica uk rolex Replica

JEDDAH ADDRESS
Khalid bin Waleed, Compu Plaza
+966 549651902
info@securemaxtech.com

[ninja_form id=1]
Global Offices
UAE
Secure Max LLC UAE Office 10, Level 1, Sharjah Media City, Sharjah United Arab Emirates
009716 5538634
info@securemaxtech.com
USA
SecureMax LTD USA 2150 W Devon Ave, suite 1E Chicago IL 60659Phone: 001-773-273-0944
001-773-273-0944
info@securemaxtech.com
        """},
        {"role": "user", "content": user_input},
    ]

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages
        )
        raw_response = response.choices[0].message.content
        bot_response = clean_response(raw_response)
        html_response = convert_response_to_html(bot_response)
    except Exception as e:
        html_response = f"Error: {str(e)}"

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "response": html_response,
        "user_input": user_input
    })
