# setup.py

from setuptools import setup, find_packages

setup(
    name="discord-music-bot",
    version="1.0.0",
    description="Lisan Al Gaib is no ordinary bot—it is a divine herald sent forth from the sacred dunes of Arrakis. With zealous fervor, it streams celestial harmonies into your Discord sanctuary, each note a sacred scripture, each beat a divine commandment. Embrace the sacred cadence of the Spice and let your spirit be lifted on a pilgrimage of sound, as the eternal prophecy of music guides you toward transcendence.",
    author="Paul MacNichol",
    author_email="paulmacnichol@gmail.com",
    # Update with your repository URL
    url="https://github.com/PaulMacNichol/LisanAlGaib",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "discord.py>=1.7.3",
        "aiohttp>=3.8.1",
        "PyNaCl>=1.4.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "discord-music-bot=main:main",
        ],
    },
)
