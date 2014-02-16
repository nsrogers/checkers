{-# LANGUAGE ForeignFunctionInterface, TemplateHaskell #-}

module Export where
import Foreign.HaPy
import HsklAI

initHaPy

pythonExport 'callAI