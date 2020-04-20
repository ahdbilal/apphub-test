#!/bin/sh

gpg --quiet --batch --yes --decrypt --passphrase="$IOS_PROFILE_KEY" --output .github/secrets/adhocprofile.mobileprovision .github/secrets/adhocprofile.mobileprovision.gpg
gpg --quiet --batch --yes --decrypt --passphrase="$IOS_PROFILE_KEY" --output .github/secrets/Certificates.p12 .github/secrets/Certificates.p12.gpg

mkdir -p ~/Library/MobileDevice/Provisioning\ Profiles

cp .github/secrets/adhocprofile.mobileprovision ~/Library/MobileDevice/Provisioning\ Profiles/acdfe2eb-e759-40ba-a4be-2c34881dc531.mobileprovision


security create-keychain -p "" build.keychain
security import .github/secrets/Certificates.p12 -t agg -k ~/Library/Keychains/build.keychain -P "" -A

security set-keychain-settings -t 3600 -l ~/Library/Keychains/build.keychain
security list-keychains -s ~/Library/Keychains/build.keychain
security default-keychain -s ~/Library/Keychains/build.keychain
security unlock-keychain -p "" ~/Library/Keychains/build.keychain


security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k "" ~/Library/Keychains/build.keychain
