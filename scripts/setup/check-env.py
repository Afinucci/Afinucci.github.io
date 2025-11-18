#!/usr/bin/env python3
"""
Environment validation script
Checks that all required environment variables are set
"""
import os
import sys
from pathlib import Path


class Colors:
    """Terminal colors"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def check_env_file():
    """Check if .env file exists"""
    if not Path('.env').exists():
        print(f"{Colors.RED}❌ .env file not found{Colors.NC}")
        print(f"{Colors.YELLOW}Run 'cp .env.example .env' and configure it{Colors.NC}")
        return False
    return True


def check_required_vars():
    """Check required environment variables"""
    required_vars = {
        'DATABASE_URL': 'Database connection string',
        'REDIS_URL': 'Redis connection string',
        'SECRET_KEY': 'Application secret key',
        'OPENAI_API_KEY': 'OpenAI API key (for AI features)',
    }

    optional_vars = {
        'ANTHROPIC_API_KEY': 'Anthropic Claude API key',
        'PINECONE_API_KEY': 'Pinecone vector database key',
        'PINECONE_ENVIRONMENT': 'Pinecone environment',
    }

    print(f"\n{Colors.BLUE}📋 Checking environment variables...{Colors.NC}\n")

    # Check required variables
    missing_required = []
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value or value == 'your-' + var.lower().replace('_', '-'):
            print(f"{Colors.RED}❌ {var}{Colors.NC} - {description}")
            missing_required.append(var)
        else:
            print(f"{Colors.GREEN}✓ {var}{Colors.NC} - {description}")

    print()

    # Check optional variables
    missing_optional = []
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if not value or value == 'your-' + var.lower().replace('_', '-'):
            print(f"{Colors.YELLOW}⚠ {var}{Colors.NC} - {description} (optional)")
            missing_optional.append(var)
        else:
            print(f"{Colors.GREEN}✓ {var}{Colors.NC} - {description}")

    print()

    # Summary
    if missing_required:
        print(f"{Colors.RED}❌ Missing {len(missing_required)} required variables:{Colors.NC}")
        for var in missing_required:
            print(f"   - {var}")
        print()
        return False

    if missing_optional:
        print(f"{Colors.YELLOW}⚠ Missing {len(missing_optional)} optional variables:{Colors.NC}")
        for var in missing_optional:
            print(f"   - {var}")
        print(f"\n{Colors.YELLOW}Some features may not work without these.{Colors.NC}\n")

    print(f"{Colors.GREEN}✅ All required environment variables are set!{Colors.NC}\n")
    return True


def check_ai_keys():
    """Check AI service API keys"""
    openai_key = os.getenv('OPENAI_API_KEY', '')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')

    if not openai_key.startswith('sk-') and not anthropic_key.startswith('sk-ant-'):
        print(f"{Colors.YELLOW}⚠ Warning: No valid AI API keys detected{Colors.NC}")
        print("AI features will not work without valid API keys")
        print("Get keys from:")
        print("  - OpenAI: https://platform.openai.com/api-keys")
        print("  - Anthropic: https://console.anthropic.com/")
        print()
        return False
    return True


def main():
    """Main function"""
    print(f"\n{Colors.BLUE}🔍 WWS Inventory Platform - Environment Check{Colors.NC}")
    print("=" * 60)

    if not check_env_file():
        sys.exit(1)

    # Load .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print(f"{Colors.YELLOW}⚠ python-dotenv not installed, reading from environment{Colors.NC}\n")

    if not check_required_vars():
        print(f"{Colors.RED}Please configure missing variables in .env file{Colors.NC}\n")
        sys.exit(1)

    check_ai_keys()

    print("=" * 60)
    print(f"{Colors.GREEN}🎉 Environment configuration looks good!{Colors.NC}\n")


if __name__ == '__main__':
    main()
