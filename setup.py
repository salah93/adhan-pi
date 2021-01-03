from setuptools import find_packages, setup


######

CLASSIFIERS = [
    "Programming Language :: Python",
    "License :: OSI Approved :: MIT License",
]
DESCRIPTION = ""
KEYWORDS = ["python"]
URL = ""
AUTHOR = "Salah Ahmed"
AUTHOR_EMAIL = "salahs.email@pm.me"

REQUIREMENTS = ["attr", "geopy", "requests"]
TEST_REQUIREMENTS = ["pytest-cov", "coverage[toml]"]
DEV_REQUIREMENTS = [
    "ipython",
    "jedi==0.17.2",
    "pdbpp",
    "black",
    "flake8",
    "pre-commit",
    "tox",
]

#####

with open("README.rst", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="adhan_pi",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/rst",
    classifiers=CLASSIFIERS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    keywords=KEYWORDS,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    entry_points={
        "console_scripts": [
            "schedule_prayer_cron=adhan_pi.cli:schedule_prayer_cron",
            "alert_adhan=adhan_pi.cli:alert_adhan",
        ],
    },
    extras_require={
        "test": TEST_REQUIREMENTS,
        "dev": TEST_REQUIREMENTS + DEV_REQUIREMENTS,
        "cron": ["python-crontab", "pydub"],
    },
)
