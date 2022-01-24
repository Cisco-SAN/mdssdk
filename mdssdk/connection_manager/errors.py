import logging

log = logging.getLogger(__name__)


class NXOSError(Exception):
    """ """

    def __init__(self, message):
        """

        :param message:
        """

        self.message = message.strip()

    def __repr__(self):
        """

        :return:
        """
        return "%s: %s" % (self.__class__.__name__, self.message)

    __str__ = __repr__


class CLIError(NXOSError):
    """ """

    def __init__(self, command, message):
        """

        :param command:
        :param message:
        """
        self.command = command.strip()
        self.message = message.strip()

    def __repr__(self):
        """

        :return:
        """
        return 'The command " %s " gave the error " %s ".' % (
            self.command,
            self.message,
        )

    __str__ = __repr__


class SSHException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class CustomException(Exception):
    """ """

    def __init__(self, message):
        """

        :param message:
        """
        self.message = message.strip()

    def __repr__(self):
        """

        :return:
        """
        return "%s: %s" % (self.__class__.__name__, self.message)

    __str__ = __repr__


class UnsupportedVersion(CustomException):
    pass


class VersionNotFound(CustomException):
    pass


class UnsupportedSwitch(CustomException):
    pass


class UnsupportedSeedSwitch(CustomException):
    pass


class UnsupportedFeature(CustomException):
    pass


class FeatureNotEnabled(CustomException):
    pass


class UnsupportedConfig(CustomException):
    pass


class VsanNotPresent(CustomException):
    pass


class InvalidInterface(CustomException):
    pass


# Analytics related exceptions
class InvalidProfile(CustomException):
    pass


class InvalidAnalyticsType(CustomException):
    pass


class InvalidMode(CustomException):
    pass


# portchannel related exceptions
class PortChannelNotPresent(CustomException):
    pass


class InvalidPortChannelRange(CustomException):
    pass


class InvalidChannelMode(CustomException):
    pass


# zone related exceptions
class InvalidZoneMode(CustomException):
    pass


class InvalidDefaultZone(CustomException):
    pass


class InvalidZoneMemberType(CustomException):
    pass
